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
            campl.AMPL_DataFrameArrowFree(&self._c_df)


    cdef void init_from_arrow(self,
                              campl.ArrowSchema* schema_ptr,
                              campl.ArrowArray* array_ptr,
                              int64_t nindices):
        cdef campl.AMPL_ERRORINFO* errorinfo
        errorinfo = campl.AMPL_DataFrameArrowCreate(&self._c_df,
                                                    schema_ptr,
                                                    array_ptr,
                                                    nindices)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

    cdef campl.AMPL_DATAFRAMEARROW* get_ptr(self):
        return self._c_df

    def _consume_stream(self):
        """Create a nanoarrow stream from the stored Arrow data (one-shot)."""
        cdef campl.ArrowSchema* schema_ptr = (<campl.ArrowSchema**>self._c_df)[0]
        cdef campl.ArrowArray* array_ptr = (<campl.ArrowArray**>self._c_df)[1]
        capsule_schema = PyCapsule_New(<void*>schema_ptr, "arrow_schema", NULL)
        capsule_array = PyCapsule_New(<void*>array_ptr, "arrow_array", NULL)
        return c_array_stream(capsule_array, capsule_schema)

    def _read_columns(self):
        """Return (nindices, col_names, col_data) using pyarrow."""
        assert pa is not None, "pyarrow is required"
        cdef int64_t nindices = 0
        campl.AMPL_DataFrameArrowGetNIndices(self._c_df, &nindices)
        stream = self._consume_stream()
        table = pa.RecordBatchReader.from_stream(stream).read_all()
        col_names = table.schema.names
        col_data  = [table.column(i).to_pylist() for i in range(len(col_names))]
        return nindices, col_names, col_data

    #@classmethod
    #def from_polars(cls, df, index_names=None, indexarity=None):
    #    """
    #    Create a :class:`~amplpy.DataFrameArrow` from a Polars DataFrame.
    #    """
    #    assert pl is not None and isinstance(df, pl.DataFrame)
    #    stream = na.c_array_stream(df.to_arrow())

    #    c_schema_capsule = stream.get_schema().__arrow_c_schema__()
    #    _, c_array_capsule = stream.get_next().__arrow_c_array__()

    #    cdef const campl.ArrowSchema* schema_ptr = <const campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
    #    cdef const campl.ArrowArray* array_ptr = <const campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

    #    cdef DataFrameArrow obj = DataFrameArrow()

    #    cdef int64_t nindices = (len(df.columns) - 1) if indexarity is None else indexarity
    #    obj.init_from_arrow(schema_ptr, array_ptr, nindices)
    #    return obj

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

        if not isinstance(df.index, pd.MultiIndex) and isinstance(df.index[0], tuple):
            df.index = pd.MultiIndex.from_tuples(df.index.tolist())

        if indexarity is not None and indexarity == df.index.nlevels + 1:
            df = df.stack()
            if isinstance(df, pd.Series):
                df = pd.DataFrame(df)

        if index_names is not None:
            assert len(index_names) == df.index.nlevels
            df.index.names = index_names

        df_reset = df.reset_index()
        pa_df = pa.Table.from_pandas(df_reset, preserve_index=False)
        del df_reset
        array_stream = na.c_array_stream(pa_df)
        c_schema_capsule, c_array_capsule = array_stream.get_next().__arrow_c_array__()
        del pa_df

        cdef campl.ArrowSchema* arrow_schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef campl.ArrowArray* arrow_array_ptr = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()
        obj._capsule_schema = c_schema_capsule
        obj._capsule_array = c_array_capsule

        cdef int64_t nindices = df.index.nlevels if indexarity is None else indexarity
        obj.init_from_arrow(arrow_schema_ptr, arrow_array_ptr, nindices)
        return obj

    @classmethod
    def from_dict(cls, dic, index_names=None, column_names=None):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a dictionary.

        Keys are index values (scalar or tuple for multi-index); values are
        column values (scalar or tuple for multiple columns).

        Args:
            dic: source dictionary.
            index_names: names for the index columns.
            column_names: names for the value columns.
        """
        assert pa is not None, "pyarrow is required for from_dict"
        assert isinstance(dic, dict) and len(dic) != 0

        def _tup(e):
            return tuple(e) if isinstance(e, (tuple, list)) else (e,)

        lst_index  = list(map(_tup, dic.keys()))
        lst_values = list(map(_tup, dic.values()))
        nindices  = len(lst_index[0])
        ncolumns  = len(lst_values[0])

        if index_names is None:
            index_names = [f"index{i}" for i in range(nindices)]
        if column_names is None:
            column_names = [f"value{i}" for i in range(ncolumns)]

        data = {index_names[i]: [k[i] for k in lst_index]  for i in range(nindices)}
        data.update({column_names[i]: [v[i] for v in lst_values] for i in range(ncolumns)})

        table = pa.table(data)
        array_stream = na.c_array_stream(table)
        c_schema_capsule, c_array_capsule = array_stream.get_next().__arrow_c_array__()

        cdef campl.ArrowSchema* schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef campl.ArrowArray* array_ptr   = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()
        obj._capsule_schema = c_schema_capsule
        obj._capsule_array  = c_array_capsule
        cdef int64_t ni = nindices
        obj.init_from_arrow(schema_ptr, array_ptr, ni)
        return obj

    @classmethod
    def from_list(cls, lst, index_names, column_names):
        """
        Create a :class:`~amplpy.DataFrameArrow` from a list of rows.

        Each row must be a tuple (index values followed by column values),
        matching the format returned by :meth:`to_list`.

        Args:
            lst: list of row tuples.
            index_names: names for the index columns.
            column_names: names for the value columns.
        """
        assert pa is not None, "pyarrow is required for from_list"
        assert len(lst) != 0

        nindices = len(index_names)
        ncolumns = len(column_names)

        def _tup(e):
            return tuple(e) if isinstance(e, (tuple, list)) else (e,)

        rows       = list(map(_tup, lst))
        index_vals = [r[:nindices] for r in rows]
        col_vals   = [r[nindices:] for r in rows]

        data = {index_names[i]: [k[i] for k in index_vals] for i in range(nindices)}
        data.update({column_names[i]: [v[i] for v in col_vals] for i in range(ncolumns)})

        table = pa.table(data)
        array_stream = na.c_array_stream(table)
        c_schema_capsule, c_array_capsule = array_stream.get_next().__arrow_c_array__()

        cdef campl.ArrowSchema* schema_ptr = <campl.ArrowSchema*>PyCapsule_GetPointer(c_schema_capsule, "arrow_schema")
        cdef campl.ArrowArray* array_ptr   = <campl.ArrowArray*>PyCapsule_GetPointer(c_array_capsule, "arrow_array")

        cdef DataFrameArrow obj = DataFrameArrow()
        obj._capsule_schema = c_schema_capsule
        obj._capsule_array  = c_array_capsule
        cdef int64_t ni = nindices
        obj.init_from_arrow(schema_ptr, array_ptr, ni)
        return obj

    def to_dict(self):
        """
        Return a dictionary with the DataFrame data.

        Keys are index values (scalar for single index, tuple for multi-index).
        Values are scalar for one value column, or a tuple for multiple columns.
        """
        nindices, col_names, col_data = self._read_columns()
        if nindices == 0:
            raise ValueError("cannot convert to dictionary without an index")
        ncols  = len(col_data) - nindices
        nrows  = len(col_data[0])
        result = {}
        for i in range(nrows):
            key = col_data[0][i] if nindices == 1 else tuple(col_data[j][i] for j in range(nindices))
            if ncols == 0:
                result[key] = None
            elif ncols == 1:
                result[key] = col_data[nindices][i]
            else:
                result[key] = tuple(col_data[nindices + j][i] for j in range(ncols))
        return result

    def to_list(self, skip_index=False):
        """
        Return a list with the DataFrame data.

        Each element is a tuple of the full row (index + values). If the total
        number of columns is 1, a plain scalar is returned per row instead of a
        1-element tuple.

        Args:
            skip_index: set to True to retrieve only value columns.
        """
        nindices, col_names, col_data = self._read_columns()
        ncols_total = len(col_data)
        nrows = len(col_data[0]) if col_data else 0

        if skip_index:
            n_val = ncols_total - int(nindices)
            ni = int(nindices)
            if n_val == 1:
                return list(col_data[ni])
            else:
                return [tuple(col_data[ni + j][i] for j in range(n_val)) for i in range(nrows)]

        if ncols_total > 1:
            return [tuple(col_data[j][i] for j in range(ncols_total)) for i in range(nrows)]
        else:
            return [col_data[0][i] for i in range(nrows)]

    def to_pandas(self, multi_index=True):
        """
        Convert this :class:`~amplpy.DataFrameArrow` to a :class:`pandas.DataFrame`.
        """
        assert pd is not None, "pandas is required for to_pandas"
        cdef int64_t nindices = 0
        campl.AMPL_DataFrameArrowGetNIndices(self._c_df, &nindices)
        stream = self._consume_stream()
        if pa is not None:
            table = pa.RecordBatchReader.from_stream(stream).read_all()
            # self_destruct frees each Arrow column buffer as it is converted,
            # so the Arrow table and the pandas DataFrame are never both fully
            # resident in memory at the same time.
            flat = table.to_pandas(self_destruct=True)
            del table
        else:
            arr = na.Array(stream)
            col_names = [f.name for f in arr.schema.fields]
            flat = pd.DataFrame({
                name: arr.child(i).to_pylist()
                for i, name in enumerate(col_names)
            })
        if nindices > 0 and nindices < len(flat.columns):
            index_cols = list(flat.columns[:nindices])
            if nindices == 1:
                flat = flat.set_index(index_cols[0])
            elif multi_index:
                flat = flat.set_index(index_cols)
            else:
                tuples = list(zip(*[flat[c] for c in index_cols]))
                flat.index = pd.Index(pd.Series(tuples, dtype=object))
                flat = flat.drop(columns=index_cols)
        return flat

    def to_polars(self):
        """
        Convert this :class:`~amplpy.DataFrameArrow` to a :class:`polars.DataFrame`.
        """
        assert pl is not None, "polars is required for to_polars"
        stream = self._consume_stream()
        return pl.from_arrow(stream)
