# -*- coding: utf-8 -*-
from numbers import Real
from collections.abc import Iterable


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
        PY_AMPL_CALL(campl.AMPL_ParameterIsSymbolic(self._ampl._c_ampl, self._name, &value))
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
        PY_AMPL_CALL(campl.AMPL_ParameterHasDefault(self._ampl._c_ampl, self._name, &value))
        return value

    def __getitem__(self, index):
        if not isinstance(index, (tuple, list)):
            index = [index]
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_TUPLE* tuple_c =  to_c_tuple(index)
        cdef char* expression
        cdef campl.AMPL_VARIANT* v
        errorinfo = campl.AMPL_InstanceGetName(self._ampl._c_ampl, self._name, tuple_c, &expression)
        campl.AMPL_TupleFree(&tuple_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        errorinfo = campl.AMPL_GetValue(self._ampl._c_ampl, expression, &v)
        campl.AMPL_StringFree(&expression)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        py_variant = to_py_variant(v)
        campl.AMPL_VariantFree(&v)
        return py_variant

    def value(self):
        """
        Get the value of this parameter. Valid only for non-indexed parameters.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_VARIANT* v
        errorinfo = campl.AMPL_GetValue(self._ampl._c_ampl, self._name, &v)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
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
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_TUPLE* index_c
        if len(args) == 1:
            value = args[0]
    
            if isinstance(value, Real):
                errorinfo = campl.AMPL_ParameterSetNumeric(self._ampl._c_ampl, self._name, float(value))
            elif isinstance(value, str):
                errorinfo = campl.AMPL_ParameterSetString(self._ampl._c_ampl, self._name, value.encode('utf-8'))
            else:
                raise TypeError
        else:
            index, value = args
            if not isinstance(index, (tuple, list)):
                index = [index]
            index_c = to_c_tuple(index)
            if isinstance(value, Real):
                errorinfo = campl.AMPL_ParameterInstanceSetNumericValue(self._ampl._c_ampl, self._name, index_c, float(value))
                campl.AMPL_TupleFree(&index_c)
            elif isinstance(value, str):
                errorinfo = campl.AMPL_ParameterInstanceSetStringValue(self._ampl._c_ampl, self._name, index_c, value.encode('utf-8'))
                campl.AMPL_TupleFree(&index_c)
            else:
                campl.AMPL_TupleFree(&index_c)
                raise TypeError
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

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
        cdef campl.AMPL_ERRORINFO* errorinfo
        if isinstance(values, dict):
            if not values:
                return
            errorinfo = setValuesPyDict(self._ampl._c_ampl, self._name, values)
            if errorinfo:
                PY_AMPL_CALL(errorinfo)
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
                errorinfo = setValuesParamStr(self._ampl._c_ampl, self._name, values)
                if errorinfo:
                    PY_AMPL_CALL(errorinfo)
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                errorinfo = setValuesParamNum(self._ampl._c_ampl, self._name, values)
                if errorinfo:
                    PY_AMPL_CALL(errorinfo)
            else:
                Entity.set_values(self, values)
        else:
            Entity.set_values(self, values)

    # Aliases
    hasDefault = has_default
    isSymbolic = is_symbolic
    setValues = set_values
