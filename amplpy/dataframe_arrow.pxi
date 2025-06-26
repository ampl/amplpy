# -*- coding: utf-8 -*-
from libc.stdlib cimport malloc, free
from libc.string cimport strdup

from cpython.float cimport PyFloat_AsDouble
from cpython.long cimport PyLong_AsLong, PyLong_Check
from cpython.exc cimport PyErr_Occurred, PyErr_Clear
from libc.stdint cimport int64_t

from numbers import Real

from nanoarrow import c_array, c_schema, c_array_stream


try:
    import pandas as pd
except ImportError:
    pd = None
try :
    import polars as pl
except ImportError:
    pl = None
try:
    import numpy as np
except ImportError:
    np = None


cdef class DataFrameArrow:
    cdef campl.AMPL_DATAFRAMEARROW* _c_df

    def __cinit__(self):
        self._c_df = NULL

    def __dealloc__(self):
        if self._c_df != NULL:
            #campl.AMPL_DataFrameArrowFree(&self._c_df)
            self._c_df = NULL

    cdef void init_from_arrow(self, const campl.ArrowSchema* schema_ptr, const campl.ArrowArray* array_ptr, int64_t nindices):
        cdef campl.AMPL_ERRORINFO* errorinfo
        errorinfo = campl.AMPL_DataFrameArrowCreate(&self._c_df, schema_ptr, array_ptr, nindices)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

    cdef campl.AMPL_DATAFRAMEARROW* get_ptr(self):
        return self._c_df

    @classmethod
    def from_polars(cls, df):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a Polars DataFrame.
        """
        assert isinstance(df, pl.DataFrame)

        stream = na.c_array_stream(df.to_arrow())
        c_schema_capsule = stream.get_schema().__arrow_c_schema__()
        _, c_array_capsule = stream.get_next().__arrow_c_array__()

        cdef const campl.ArrowSchema* arrow_schema_ptr
        cdef const campl.ArrowArray* arrow_array_ptr
        arrow_schema_ptr = <const campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        arrow_array_ptr = <const campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()
        obj.init_from_arrow(arrow_schema_ptr, arrow_array_ptr, 0)
        return obj

    @classmethod
    def from_pandas(cls, df):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a Polars DataFrame.
        """
        assert isinstance(df, pl.DataFrame)

        stream = na.c_array_stream(df.to_arrow())
        c_schema_capsule = stream.get_schema().__arrow_c_schema__()
        _, c_array_capsule = stream.get_next().__arrow_c_array__()

        cdef const campl.ArrowSchema* arrow_schema_ptr
        cdef const campl.ArrowArray* arrow_array_ptr
        arrow_schema_ptr = <const campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        arrow_array_ptr = <const campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()
        obj.init_from_arrow(arrow_schema_ptr, arrow_array_ptr, 0)
        return obj
