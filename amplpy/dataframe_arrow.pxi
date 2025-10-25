# -*- coding: utf-8 -*-
from libc.stdlib cimport malloc, free
from libc.string cimport strdup

from cpython.float cimport PyFloat_AsDouble
from cpython.long cimport PyLong_AsLong, PyLong_Check
from cpython.exc cimport PyErr_Occurred, PyErr_Clear
from libc.stdint cimport int64_t

from cpython.pycapsule cimport PyCapsule_IsValid

from numbers import Real

import nanoarrow as na
from nanoarrow import c_array, c_schema, c_array_stream


try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import pyarrow as pa
except ImportError:
    pa = None
try :
    import polars as pl
except ImportError:
    pl = None


cdef class DataFrameArrow:
    cdef campl.AMPL_DATAFRAMEARROW* _c_df
    cdef object _capsule_schema
    cdef object _capsule_array

    def __cinit__(self):
        self._c_df = NULL

    def __dealloc__(self):
        if self._c_df != NULL:
            # Uncomment when Free is implemented
            # campl.AMPL_DataFrameArrowFree(&self._c_df)
            self._c_df = NULL


    cdef void init_from_arrow(self,
                              campl.ArrowSchema* schema_ptr,
                              campl.ArrowArray* array_ptr,
                              int64_t nindices):
        #if array_ptr.release == NULL:
        #    raise ValueError("ArrowArray has been released — invalid memory.")
        cdef campl.AMPL_ERRORINFO* errorinfo
        errorinfo = campl.AMPL_DataFrameArrowCreate(&self._c_df,
                                                    schema_ptr,
                                                    array_ptr,
                                                    nindices)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

    cdef campl.AMPL_DATAFRAMEARROW* get_ptr(self):
        return self._c_df

    @classmethod
    def from_polars(cls, df):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a Polars DataFrame.
        """
        assert pl is not None and isinstance(df, pl.DataFrame)
        stream = na.c_array_stream(df.to_arrow())

        c_schema_capsule = stream.get_schema().__arrow_c_schema__()
        _, c_array_capsule = stream.get_next().__arrow_c_array__()

        cdef const campl.ArrowSchema* schema_ptr = <const campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef const campl.ArrowArray* array_ptr = <const campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()

        obj.init_from_arrow(schema_ptr, array_ptr, 0)
        return obj

    @classmethod
    def from_pandas(cls, df, index_names=None, indexarity=None):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a pandas DataFrame.

        Args:
            df: Pandas DataFrame or Series to load.
            index_names: Optional list of index column names.
            indexarity: Optional number of index columns.
        """
        assert None not in (pd, pa, na) and isinstance(df, (pd.DataFrame, pd.Series))

        if isinstance(df, pd.Series):
            df = pd.DataFrame(df)

        if len(df) == 0:
            raise ValueError("Cannot create DataFrameArrow from empty DataFrame")

        if isinstance(df.index[0], tuple):
            df.index = pd.MultiIndex.from_tuples(df.index.tolist())
        #elif df.index.nlevels == 1 and not isinstance(df.index, pd.MultiIndex):
        #    df.index = pd.MultiIndex.from_tuples([(idx,) for idx in df.index])

        if indexarity is not None and indexarity == df.index.nlevels + 1:
            df = df.stack()
            if isinstance(df, pd.Series):
                df = pd.DataFrame(df)

        if index_names is not None:
            assert len(index_names) == df.index.nlevels
            df.index.names = index_names

        df_reset = df.reset_index()

        pa_df = pa.Table.from_pandas(df_reset, preserve_index=False)
        array_stream = na.c_array_stream(pa_df)
        c_schema_capsule, c_array_capsule = array_stream.get_next().__arrow_c_array__()

        cdef campl.ArrowSchema* arrow_schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef campl.ArrowArray* arrow_array_ptr = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")


        cdef DataFrameArrow obj = DataFrameArrow()
        obj._capsule_schema = c_schema_capsule
        obj._capsule_array = c_array_capsule

        cdef int64_t nindices = df.index.nlevels if indexarity is None else indexarity
        obj.init_from_arrow(arrow_schema_ptr, arrow_array_ptr, nindices)
        return obj
