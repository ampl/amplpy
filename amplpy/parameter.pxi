# -*- coding: utf-8 -*-
from numbers import Real
from collections.abc import Iterable

from cpython.pycapsule cimport PyCapsule_GetPointer, PyCapsule_IsValid

import polars as pl
import pyarrow as pa
import nanoarrow as na



import itertools

try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import numpy as np
except ImportError:
    np = None



cdef class Parameter(Entity):
    """
    Represents an AMPL parameter. The values can be float or string (in case of
    symbolic parameters).

    Data can be assigned to the set using the methods
    :func:`~amplpy.Parameter.set` and
    :func:`~amplpy.Parameter.set_values`
    or using
    :func:`~amplpy.AMPL.set_data`
    and an object of class :class:`~amplpy.DataFrame`.
    """
    @staticmethod
    cdef create(AMPL ampl, char* name, campl.AMPL_TUPLE* index, parent):
        entity = Parameter()
        entity._ampl = ampl
        Py_INCREF(entity._ampl)
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_PARAMETER
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def __setitem__(self, index, value):
        self.set(index, value)

    def is_symbolic(self):
        """
        Returns True if the parameter is declared as symbolic (can store both
        numerical and string values).
        """
        cdef bool_c value
        campl.AMPL_ParameterIsSymbolic(self._ampl._c_ampl, self._name, &value)
        return value

    def has_default(self):
        """
        Check if the parameter has a default initial value. In case of the
        following AMPL code:

        .. code-block:: ampl

            param a;
            param b default a;

        the function will return true for parameter ``b``.

        Returns:
            True if the parameter has a default initial value. Please note
            that if the parameter has a default expression which refers to
            another parameter which value is not defined, this will return
            True.
        """
        cdef bool_c value
        campl.AMPL_ParameterHasDefault(self._ampl._c_ampl, self._name, &value)
        return value

    def __getitem__(self, index):
        if not isinstance(index, (tuple, list)):
            index = [index]
        cdef campl.AMPL_TUPLE* tuple_c =  to_c_tuple(index)
        cdef char* expression
        cdef campl.AMPL_VARIANT* v
        campl.AMPL_InstanceGetName(self._ampl._c_ampl, self._name, tuple_c, &expression)
        campl.AMPL_TupleFree(&tuple_c)
        campl.AMPL_GetValue(self._ampl._c_ampl, expression, &v)
        campl.AMPL_StringFree(&expression)
        py_variant = to_py_variant(v)
        campl.AMPL_VariantFree(&v)
        return py_variant

    def value(self):
        """
        Get the value of this parameter. Valid only for non-indexed parameters.
        """
        cdef campl.AMPL_VARIANT* v
        campl.AMPL_GetValue(self._ampl._c_ampl, self._name, &v)
        py_variant = to_py_variant(v)
        campl.AMPL_VariantFree(&v)
        return py_variant

    def set(self, *args):
        """
        Set the value of a single instance of this parameter.

        Args:
            args: value if the parameter is scalar, index and value
            otherwise.

        Raises:
            RuntimeError: If the entity has been deleted in the underlying
            AMPL.

            TypeError: If the parameter is not scalar and the index is not
            provided.
        """
        assert len(args) in (1, 2)
        cdef campl.AMPL_TUPLE* index_c
        if len(args) == 1:
            value = args[0]
    
            if isinstance(value, Real):
                campl.AMPL_ParameterSetNumeric(self._ampl._c_ampl, self._name, float(value))
            elif isinstance(value, str):
                campl.AMPL_ParameterSetString(self._ampl._c_ampl, self._name, value.encode('utf-8'))
            else:
                raise TypeError
        else:
            index, value = args
            if not isinstance(index, (tuple, list)):
                index = [index]
            index_c = to_c_tuple(index)
            if isinstance(value, Real):
                campl.AMPL_ParameterInstanceSetNumericValue(self._ampl._c_ampl, self._name, index_c, float(value))
                campl.AMPL_TupleFree(&index_c)
            elif isinstance(value, str):
                campl.AMPL_ParameterInstanceSetStringValue(self._ampl._c_ampl, self._name, index_c, value.encode('utf-8'))
                campl.AMPL_TupleFree(&index_c)
            else:
                campl.AMPL_TupleFree(&index_c)
                raise TypeError

    def set_values(self, values):
        """
        Assign the values (string or float) to the parameter instances with the
        specified indices, equivalent to the AMPL code:

        .. code-block:: ampl

            let {i in indices} par[i] := values[i];

        Args:
            values: list, dictionary or :class:`~amplpy.DataFrame` with the
            indices and the values to be set.

        Raises:
            TypeError: If called on a scalar parameter.
        """
        if isinstance(values, dict):
            if not values:
                return
            setValuesPyDict(self._ampl._c_ampl, self._name, values)
        elif isinstance(values, DataFrame):
            Entity.set_values(self, values)
        elif pd is not None and isinstance(values, (pd.DataFrame, pd.Series)):
            Entity.set_values(self, values)
        elif np is not None and isinstance(values, np.ndarray):
            if len(values.shape) <= 1:
                self.set_values(values.tolist())
            else:
                self.set_values(tuple(itertools.chain(*values.tolist())))
        elif isinstance(values, Iterable):
            if all(isinstance(value, str) for value in values):
                if not isinstance(values, (list, tuple)):
                    values = list(values)
                setValuesParamStr(self._ampl._c_ampl, self._name, values)
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                setValuesParamNum(self._ampl._c_ampl, self._name, values)
            else:
                Entity.set_values(self, values)
        else:
            Entity.set_values(self, values)


    def set_nanoarrow(self, df):
        array_stream = na.c_array_stream(pa.Table.from_pandas(df.reset_index(), preserve_index=False))
        c_schema_capsule, c_array_capsule = array_stream.get_next().__arrow_c_array__()

        cdef campl.ArrowSchema* arrow_schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef campl.ArrowArray* arrow_array_ptr = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        campl.AMPL_EntitySetValuesArrow(self._ampl._c_ampl, self._name, arrow_array_ptr, arrow_schema_ptr)

    def set_nanoarrowpolars(self, df):
        cdef const campl.ArrowSchema* arrow_schema_ptr
        cdef const campl.ArrowArray* arrow_array_ptr
        stream = na.c_array_stream(df.to_arrow())
        c_schema_capsule = stream.get_schema().__arrow_c_schema__()
        _, c_array_capsule = stream.get_next().__arrow_c_array__()

        arrow_schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        arrow_array_ptr = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        campl.AMPL_EntitySetValuesArrow(self._ampl._c_ampl, self._name, arrow_array_ptr, arrow_schema_ptr)

    # Aliases
    hasDefault = has_default
    isSymbolic = is_symbolic
    setValues = set_values
