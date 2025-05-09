# -*- coding: utf-8 -*-
from libc.stdlib cimport malloc, free
from libc.string cimport strdup

from cpython.float cimport PyFloat_AsDouble
from cpython.long cimport PyLong_AsLong, PyLong_Check
from cpython.exc cimport PyErr_Occurred, PyErr_Clear

from numbers import Real

try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import numpy as np
except ImportError:
    np = None


cdef class Row(object):
    """
    Represents a row in a :class:`~amplpy.DataFrame`.
    """
    cdef campl.AMPL_DATAFRAME* _df
    cdef size_t _index

    @staticmethod
    cdef create(campl.AMPL_DATAFRAME* df, size_t index):
        row = Row()
        row._df = df
        row._index = index
        return row

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        return RowIterator.create(self._df, self._index)

    def __getitem__(self, key):
        cdef campl.AMPL_VARIANT* v
        PY_AMPL_CALL(campl.AMPL_DataFrameElement(self._df, self._index, key, &v))
        return to_py_variant(v)

    def to_string(self):
        return str(list(self))

    # Aliases
    toString = to_string


cdef class Column(object):
    """
    Represents a column in a :class:`~amplpy.DataFrame`.
    """
    cdef campl.AMPL_DATAFRAME* _df
    cdef size_t _index

    @staticmethod
    cdef create(campl.AMPL_DATAFRAME* df, size_t index):
        col = Column()
        col._df = df
        col._index = index
        return col

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        return ColIterator.create(self._df, self._index)

    def to_string(self):
        return str(self.to_list())

    def to_list(self):
        py_list = []
        cdef campl.AMPL_VARIANT* v
        cdef size_t rowindex
        cdef size_t i
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumRows(self._df, &rowindex))
        for i in range(rowindex):
            PY_AMPL_CALL(campl.AMPL_DataFrameElement(self._df, i, self._index, &v))
            py_list.append(to_py_variant(v))
        return py_list

    # Aliases
    toString = to_string
    toList = to_list


cdef class DataFrame(object):
    """
    A DataFrame object, used to communicate data to and from the AMPL entities.

    .. warning::
        DataFrame objects should not be instantiated manually. For best performance
        using Python native types or Pandas DataFrames. The API takes care of the conversion
        for you in the most efficient way it finds.

    An object of this class can be used to do the following tasks:

    - Assign values to AMPL entities (once the DataFrame is populated, use
      :func:`~amplpy.AMPL.set_data` to assign its
      values to the modelling entities in its columns)
    - Get values from AMPL, decoupling the values from the AMPL entities they
      originate via
      :func:`~amplpy.Entity.get_values`.

    A DataFrame object can be created in various ways:

    - Get values from AMPL, decoupling the values from the AMPL entities they originate from
      (via :func:`~amplpy.Entity.get_values`)
    - From Pandas dataframes with :func:`~amplpy.DataFrame.from_pandas`
    - From Numpy matrices with :func:`~amplpy.DataFrame.from_numpy`
    - From Python dictionaries with :func:`~amplpy.DataFrame.from_dict`

    and can be converted to various object types:

    - Pandas dataframes with :func:`~amplpy.DataFrame.to_pandas`
    - Python dictionary with :func:`~amplpy.DataFrame.to_dict`
    - Python list with :func:`~amplpy.DataFrame.to_list`
    """
    cdef campl.AMPL_DATAFRAME* _c_df

    def __cinit__(self, index, columns=tuple(), **kwargs):
        """
        Create a new DataFrame with specifed index and column headers.

        Args:
            index: Index column;

            columns: Column headers.
        """
        cdef char** headers
        cdef size_t index_size, column_size
        if index is not None:
            if isinstance(index, str):
                index = (index,)
            if isinstance(columns, str):
                columns = (columns,)
            index_names = [col[0] if isinstance(col, tuple) else col for col in index]
            column_names = [
                col[0] if isinstance(col, tuple) else col for col in columns
            ]
            index_size = len(index_names)
            column_size = len(column_names)
            headers = <char**> malloc((index_size+column_size) * sizeof(char*))

            for i in range(index_size + column_size):
                if i < index_size:
                    temp = index_names[i].encode('utf-8')
                else:
                    temp = column_names[i - index_size].encode('utf-8')
                headers[i] = strdup(temp)

            PY_AMPL_CALL(campl.AMPL_DataFrameCreate(&self._c_df, index_size, column_size, headers))

            for i in range(index_size+column_size):
                if headers[i] != NULL:
                    free(headers[i])
            free(headers)

            for col in index:
                if isinstance(col, tuple):
                    self._set_column(col[0], col[1])
            for col in columns:
                if isinstance(col, tuple):
                    self._set_column(col[0], col[1])

    cdef campl.AMPL_DATAFRAME* get_ptr(self):
        return self._c_df

    @staticmethod
    cdef create(campl.AMPL_DATAFRAME* df_c):
        df = DataFrame(index=None)
        df._c_df = df_c
        return df

    def __dealloc__(self):
        """
        Default destructor:
        releases all the resources related to the Dataframe instance.
        """
        campl.AMPL_DataFrameFree(&self._c_df)

    def to_string(self):
        cdef char* value_c
        PY_AMPL_CALL(campl.AMPL_DataFrameToString(self._c_df, &value_c))
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)
        return value

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        # FIXME: C++ iterators for dataframes not working with SWIG.
        return (self._get_row_by_index(i) for i in range(self._get_num_rows()))

    def _get_num_cols(self):
        """
        Get the total number of columns in this dataframe (indexarity + number
        of values).

        Returns:
            The number of columns.
        """
        cdef size_t num
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumCols(self._c_df, &num))
        return int(num)

    def _get_num_rows(self):
        """
        Get the number of data rows in this dataframe.

        Returns:
            The number of rows.
        """
        cdef size_t num
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumRows(self._c_df, &num))
        return int(num)

    def _get_num_indices(self):
        """
        Get the number of indices (the indexarity) of this dataframe.

        Returns:
            The number of indices needed to access one row of this dataframe.
        """
        cdef size_t num
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumIndices(self._c_df, &num))
        return int(num)

    def _add_row(self, *value):
        """
        Add a row to the DataFrame. The size of the tuple must be equal to the
        total number of columns in the dataframe.

        Args:
           value: A single argument with a tuple containing all the values
           for the row to be added, or multiple arguments with the values for
           each column.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        if len(value) == 1 and isinstance(value[0], (tuple, list)):
            value = value[0]
        assert len(value) == self._get_num_cols()
        cdef campl.AMPL_TUPLE* tuple_c = to_c_tuple(tuple(value))
        errorinfo = campl.AMPL_DataFrameAddRow(self._c_df, tuple_c)
        campl.AMPL_TupleFree(&tuple_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

    def _add_column(self, header, values=None):
        """
        Add a new column with the corresponding header and values to the
        dataframe.

        Args:
            header: The name of the new column.

            values: A list of size :func:`~amplpy.DataFrame.getNumRows` with
            all the values of the new column.
        """   
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef size_t size = len(values)
        cdef const char** c_string_array = NULL
        cdef double* c_double_array = NULL
        if values is None:
            values = []
        if size == 0:
            PY_AMPL_CALL(campl.AMPL_DataFrameAddEmptyColumn(self._c_df, header.encode('utf-8')))
        else:
            assert len(values) == self._get_num_rows()
            if any(isinstance(value, str) for value in values):
                c_string_array = <const char**> malloc(size * sizeof(const char*))
                if not isinstance(values, (list, tuple)):
                    values = list(values)
                for i in range(size):
                    c_string_array[i] = strdup(values[i].encode('utf-8'))
                errorinfo = campl.AMPL_DataFrameAddColumnString(self._c_df, header.encode('utf-8'), c_string_array)
                for i in range(size):
                    if c_string_array[i] != NULL:
                        free(c_string_array[i])
                free(c_string_array)
                if errorinfo:
                    PY_AMPL_CALL(errorinfo)
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                c_double_array = <double*> malloc(size * sizeof(double))
                for i in range(size):
                    c_double_array[i] = values[i]
                errorinfo = campl.AMPL_DataFrameAddColumnDouble(self._c_df, header.encode('utf-8'), c_double_array)
                free(c_double_array)
                if errorinfo:
                    PY_AMPL_CALL(errorinfo)
            else:
                raise NotImplementedError

    def _get_column(self, header):
        """
        Get the specified column as a view object.

        Args:
            header: The header of the column.
        """
        cdef size_t index
        PY_AMPL_CALL(campl.AMPL_DataFrameGetColumnIndex(self._c_df, header.encode('utf-8'), &index))
        return Column.create(self._c_df, index)

    def _set_column(self, header, values):
        """
        Set the values of a column.

        Args:
            header: The header of the column to be set.

            values: The values to set.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef double* c_double_array = NULL
        cdef char** c_string_array = NULL
        cdef size_t size = len(values)
        if isinstance(values[0], str):
            c_string_array = <char**> malloc(size * sizeof(char*))
            for i in range(size):
                c_string_array[i] = strdup(values[i].encode('utf-8'))
            errorinfo = campl.AMPL_DataFrameSetColumnArgString(self._c_df, header.encode('utf-8'), c_string_array, size)
            for i in range(size):
                if c_string_array[i] != NULL:
                    free(c_string_array[i])
            free(c_string_array)
            if errorinfo:
                PY_AMPL_CALL(errorinfo)
        else:
            c_double_array = <double*> malloc(size * sizeof(double))
            for i in range(size):
                if PyLong_Check(values[i]):
                    c_double_array[i] = PyLong_AsLong(values[i]);
                else:
                    PyErr_Clear()
                    c_double_array[i] = PyFloat_AsDouble(values[i]);
                    if PyErr_Occurred():
                        raise TypeError("Failed to cast value to int/float/double")
            errorinfo = campl.AMPL_DataFrameSetColumnArgDouble(self._c_df, header.encode('utf-8'), c_double_array, size)
            free(c_double_array)
            if errorinfo:
                PY_AMPL_CALL(errorinfo)

    def _get_row(self, key):
        """
        Get a row by value of the indexing columns. If the index is not
        specified, gets the only row of a dataframe with no indexing columns.

        Args:
            key: Tuple representing the index of the desired row.

        Returns:
            The row.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef size_t index
        cdef campl.AMPL_TUPLE* tuple = to_c_tuple(key)
        errorinfo = campl.AMPL_DataFrameGetRowIndex(self._c_df, tuple, &index)
        campl.AMPL_TupleFree(&tuple)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        return Row.create(self._c_df, index)

    def _get_row_by_index(self, index):
        """
        Get row by numeric index.

        Args:
            index: Zero-based index of the row to get.

        Returns:
            The corresponding row.
        """
        return Row.create(self._c_df, index)

    def _get_headers(self):
        """
        Get the headers of this DataFrame.

        Returns:
           The headers of this DataFrame.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef size_t size
        cdef char** headers
        errorinfo = campl.AMPL_DataFrameGetHeaders(self._c_df, &size, &headers)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        headers_py = tuple(str(headers[i].decode('utf-8')) for i in range(size))
        for i in range(size):
            campl.AMPL_StringFree(&headers[i])
        free(headers)
        return headers_py

    def _set_values(self, values):
        """
        Set the values of a DataFrame from a dictionary.

        Args:
            values: Dictionary with the values to set.
        """
        ncols = self._get_num_cols()
        nindices = self._get_num_indices()

        def conv_to_list(value):
            if isinstance(value, list):
                return value
            elif isinstance(value, tuple):
                return list(value)
            else:
                return [value]

        for key, value in values.items():
            key = conv_to_list(key)
            assert len(key) == nindices
            value = conv_to_list(value)
            assert len(value) == ncols - nindices
            self._add_row(key + value)

    def to_dict(self):
        """
        Return a dictionary with the DataFrame data.
        """
        d = {}
        nindices = self._get_num_indices()
        if nindices == 0:
            raise ValueError("cannot convert to dictionary without an index")
        data = zip(
            *[self._get_column(header).to_list() for header in self._get_headers()]
        )
        for row in data:
            if nindices == 1:
                key = row[0]
            else:
                key = tuple(row[:nindices])
            if len(row) - nindices == 0:
                d[key] = None
            elif len(row) - nindices == 1:
                d[key] = row[nindices]
            else:
                d[key] = tuple(row[nindices:])
        return d

    def to_list(self, skip_index=False):
        """
        Return a list with the DataFrame data.

        Args:
            skip_index: set to True to retrieve only values.
        """
        if self._get_num_cols() > 1:
            lst = [
                tuple(self._get_row_by_index(i)) for i in range(self._get_num_rows())
            ]
        else:
            lst = [self._get_row_by_index(i)[0] for i in range(self._get_num_rows())]
        if skip_index:
            ncols = self._get_num_cols()
            nindices = self._get_num_indices()
            if ncols - nindices == 1:
                return [row[len(row)-1] for row in lst]
            else:
                return [row[nindices:] for row in lst]
        else:
            return lst

    def to_pandas(self, multi_index=True):
        """
        Return a pandas.DataFrame with the DataFrame data.
        """
        assert pd is not None
        nindices = self._get_num_indices()
        headers = self._get_headers()
        columns = {
            header: self._get_column(header).to_list() for header in headers[nindices:]
        }
        index_names = headers[:nindices]
        if len(index_names) >= 2 and multi_index is True:
            index = pd.MultiIndex.from_arrays(
                [self._get_column(header).to_list() for header in index_names],
                names=index_names,
            )
            return pd.DataFrame(columns, index=index)
        else:
            index = zip(*[self._get_column(header).to_list() for header in index_names])
            index = [key if len(key) > 1 else key[0] for key in index]
            if index == []:
                return pd.DataFrame(columns, index=None)
            else:
                return pd.DataFrame(columns, index=index)

    @classmethod
    def from_dict(cls, dic, index_names=None, column_names=None):
        """
        Create a :class:`~amplpy.DataFrame` from a dictionary.

        Args:
            dic: dictionary to load.
            index_names: index names to use.
            column_names: column names to use.
        """
        assert isinstance(dic, dict)
        assert len(dic) != 0

        def to_tuple(e):
            if isinstance(e, (tuple, list)):
                return tuple(e)
            else:
                return (e,)

        lst_index = list(map(to_tuple, dic.keys()))
        lst_columns = list(map(to_tuple, dic.values()))
        nindices, ncolumns = len(lst_index[0]), len(lst_columns[0])
        assert index_names is None or nindices == len(index_names)
        assert column_names is None or ncolumns == len(column_names)
        assert all(len(k) == nindices for k in lst_index)
        assert all(len(v) == ncolumns for v in lst_columns)

        index = zip(*lst_index)
        columns = zip(*lst_columns)

        if index_names is None:
            index_names = [f"index{i}" for i in range(nindices)]

        if column_names is None:
            column_names = [f"value{i}" for i in range(ncolumns)]

        index = [(index_names[i], cindex) for i, cindex in enumerate(zip(*lst_index))]
        columns = [
            (column_names[i], column) for i, column in enumerate(zip(*lst_columns))
        ]
        return cls(index=index, columns=columns)

    @classmethod
    def from_pandas(cls, df, index_names=None, indexarity=None):
        """
        Create a :class:`~amplpy.DataFrame` from a pandas DataFrame.

        Args:
            df: Pandas DataFrame to load.
            index_names: index names to use.
        """
        assert pd is not None
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df)
        else:
            assert isinstance(df, pd.DataFrame)
        if len(df) == 0:
            return cls(index=df.index.names, columns=df.columns.tolist())
        if isinstance(df.index[0], tuple):
            df.index = pd.MultiIndex.from_tuples(df.index.tolist())
        if indexarity == df.index.nlevels + 1:
            df = df.stack()
            if isinstance(df, pd.Series):
                df = pd.DataFrame(df)
        if isinstance(df.index[0], tuple):
            keys = df.index.tolist()
        else:
            keys = [(key,) for key in df.index]
        index = [(f"index{i}", cindex) for i, cindex in enumerate(zip(*keys))]
        if index_names is not None:
            assert len(index) == len(index_names)
            for i in range(len(index)):
                index[i] = (index_names[i], index[i][1])
        columns = [(str(cname), df[cname].tolist()) for cname in df.columns.tolist()]
        return cls(index=index, columns=columns)

    @classmethod
    def from_numpy(cls, data):
        """
        Create a :class:`~amplpy.DataFrame` from a numpy array or matrix.
        """
        assert np is not None
        if isinstance(data, np.ndarray):
            index = []
            if len(data.shape) == 1:
                columns = [("value", data.tolist())]
            elif len(data.shape) == 2:
                columns = [(f"c{i}", col) for i, col in enumerate(zip(*data.tolist()))]
            else:
                raise TypeError
        else:
            raise TypeError
        return cls(index=index, columns=columns)

    @classmethod
    def _from_data_frame_ref(cls, df_ref):
        return cls(None, None, _impl=df_ref)

    # Aliases
    _addColumn = _add_column
    _addRow = _add_row
    _getColumn = _get_column
    _getHeaders = _get_headers
    _getNumCols = _get_num_cols
    _getNumIndices = _get_num_indices
    _getNumRows = _get_num_rows
    _getRow = _get_row
    _getRowByIndex = _get_row_by_index
    _setColumn = _set_column
    _setValues = _set_values
    fromDict = from_dict
    fromNumpy = from_numpy
    fromPandas = from_pandas
    toDict = to_dict
    toList = to_list
    toPandas = to_pandas
    toString = to_string
