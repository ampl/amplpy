# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
from builtins import map, range, zip
from numbers import Real
from past.builtins import basestring

from .base import BaseClass
from .iterators import RowIterator, ColIterator
from . import amplpython

try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import numpy as np
except ImportError:
    np = None


class Row(BaseClass):
    """
    Represents a row in a :class:`~amplpy.DataFrame`.
    """

    def __iter__(self):
        return RowIterator(self._impl)

    def __getitem__(self, key):
        return self._impl.getIndex(key)

    def to_string(self):
        return str(list(self))

    # Aliases
    toString = to_string


class Column(BaseClass):
    """
    Represents a column in a :class:`~amplpy.DataFrame`.
    """

    def __iter__(self):
        return ColIterator(self._impl)

    def to_string(self):
        return str(self.to_list())

    def to_list(self):
        return self._impl.toPyList()

    # Aliases
    toString = to_string
    toList = to_list


class DataFrame(BaseClass):
    """
    A DataFrame object, used to communicate data to and from the AMPL entities.

    An object of this class can be used to do the following tasks:
    - Assign values to AMPL entities (once the DataFrame is populated, use
    :func:`~amplpy.AMPL.set_data` / :func:`~amplpy.AMPL.setData` to assign its
    values to the modelling entities in its columns)
    - Get values from AMPL, decoupling the values from the AMPL entities they
    originate via
    :func:`~amplpy.Entity.get_values` / :func:`~amplpy.Entity.getValues`.

    A DataFrame object can be created in various ways.

    - Create a skeleton by specifiying manually the indexing columns and the
      column headers.
    - Get values from AMPL, decoupling the values from the AMPL entities they
      originate from
      (via :func:`~amplpy.Entity.get_values` / :func:`~amplpy.Entity.getValues`).

    Populating a DataFrame object can be done adding row by row to a
    pre-existing skeleton via :func:`~amplpy.DataFrame.addRow`, setting whole
    columns of a pre-existing skeleton via
    :func:`~amplpy.DataFrame.set_column` / :func:`~amplpy.DataFrame.setColumn`
    or adding columns (including indexing columns) via
    :func:`~amplpy.DataFrame.add_column` / :func:`~amplpy.DataFrame.addColumn`.

    Modifying a DataFrame object can be done via
    :func:`~amplpy.DataFrame.set_column` / :func:`~amplpy.DataFrame.setColumn`
    or, item by item, via
    :func:`~amplpy.DataFrame.set_values` / :func:`~amplpy.DataFrame.setValues`.

    Accessing data in a DataFrame can be done row by row using
    :func:`~amplpy.DataFrame.get_row` / :func:`~amplpy.DataFrame.getRow`
    or by column via
    :func:`~amplpy.DataFrame.get_column` / :func:`~amplpy.DataFrame.getColumn`.
    """

    def __init__(self, index, columns=tuple(), **kwargs):
        """
        Create a new DataFrame with specifed index and column headers.

        Args:
            index: Index column;

            columns: Column headers.
        """
        if index is not None:
            if isinstance(index, basestring):
                index = (index,)
            if isinstance(columns, basestring):
                columns = (columns,)
            index_names = [col[0] if isinstance(col, tuple) else col for col in index]
            column_names = [
                col[0] if isinstance(col, tuple) else col for col in columns
            ]
            impl = amplpython.DataFrame.factory(
                len(index_names),
                list(index_names) + list(column_names),
                len(index_names) + len(column_names),
            )
            super(DataFrame, self).__init__(impl)
            for col in index:
                if isinstance(col, tuple):
                    self.set_column(col[0], col[1])
            for col in columns:
                if isinstance(col, tuple):
                    self.set_column(col[0], col[1])
        else:
            impl = kwargs.get("_impl", None)
            super(DataFrame, self).__init__(impl)

    def __iter__(self):
        # FIXME: C++ iterators for dataframes not working with SWIG.
        return (self.get_row_by_index(i) for i in range(self.get_num_rows()))

    def get_num_cols(self):
        """
        Get the total number of columns in this dataframe (indexarity + number
        of values).

        Returns:
            The number of columns.
        """
        return self._impl.getNumCols()

    def get_num_rows(self):
        """
        Get the number of data rows in this dataframe.

        Returns:
            The number of rows.
        """
        return self._impl.getNumRows()

    def get_num_indices(self):
        """
        Get the number of indices (the indexarity) of this dataframe.

        Returns:
            The number of indices needed to access one row of this dataframe.
        """
        return self._impl.getNumIndices()

    def add_row(self, *value):
        """
        Add a row to the DataFrame. The size of the tuple must be equal to the
        total number of columns in the dataframe.

        Args:
           value: A single argument with a tuple containing all the values
           for the row to be added, or multiple arguments with the values for
           each column.
        """
        if len(value) == 1 and isinstance(value[0], (tuple, list)):
            value = value[0]
        assert len(value) == self.get_num_cols()
        self._impl.addRow(tuple(value))

    def add_column(self, header, values=None):
        """
        Add a new column with the corresponding header and values to the
        dataframe.

        Args:
            header: The name of the new column.

            values: A list of size :func:`~amplpy.DataFrame.getNumRows` with
            all the values of the new column.
        """
        if values is None:
            values = []
        if len(values) == 0:
            self._impl.addColumn(header)
        else:
            assert len(values) == self.get_num_rows()
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                self._impl.addColumnStr(header, values)
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                self._impl.addColumnDbl(header, values)
            else:
                raise NotImplementedError

    def get_column(self, header):
        """
        Get the specified column as a view object.

        Args:
            header: The header of the column.
        """
        return Column(self._impl.getColumn(header))

    def set_column(self, header, values):
        """
        Set the values of a column.

        Args:
            header: The header of the column to be set.

            values: The values to set.
        """
        self._impl.setColumnPyList(header, list(values))

    def get_row(self, key):
        """
        Get a row by value of the indexing columns. If the index is not
        specified, gets the only row of a dataframe with no indexing columns.

        Args:
            key: Tuple representing the index of the desired row.

        Returns:
            The row.
        """
        return Row(self._impl.getRowTpl(key))

    def get_row_by_index(self, index):
        """
        Get row by numeric index.

        Args:
            index: Zero-based index of the row to get.

        Returns:
            The corresponding row.
        """
        return Row(self._impl.getRowByIndex(index))

    def get_headers(self):
        """
        Get the headers of this DataFrame.

        Returns:
           The headers of this DataFrame.
        """
        return tuple(self._impl.getHeaders())

    def set_values(self, values):
        """
        Set the values of a DataFrame from a dictionary.

        Args:
            values: Dictionary with the values to set.
        """
        ncols = self.get_num_cols()
        nindices = self.get_num_indices()

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
            self.add_row(key + value)

    def to_dict(self):
        """
        Return a dictionary with the DataFrame data.
        """
        d = {}
        nindices = self.get_num_indices()
        if nindices == 0:
            raise ValueError("cannot convert to dictionary without an index")
        data = zip(
            *[self.get_column(header).to_list() for header in self.get_headers()]
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

    def to_list(self):
        """
        Return a list with the DataFrame data.
        """
        if self.get_num_cols() > 1:
            return [tuple(self.get_row_by_index(i)) for i in range(self.get_num_rows())]
        else:
            return [self.get_row_by_index(i)[0] for i in range(self.get_num_rows())]

    def to_pandas(self):
        """
        Return a pandas DataFrame with the DataFrame data.
        """
        assert pd is not None
        nindices = self.get_num_indices()
        headers = self.get_headers()
        columns = {
            header: self.get_column(header).to_list() for header in headers[nindices:]
        }
        index = zip(
            *[self.get_column(header).to_list() for header in headers[:nindices]]
        )
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
            index_names = ["index{}".format(i) for i in range(nindices)]

        if column_names is None:
            column_names = ["value{}".format(i) for i in range(ncolumns)]

        index = [(index_names[i], cindex) for i, cindex in enumerate(zip(*lst_index))]
        columns = [
            (column_names[i], column) for i, column in enumerate(zip(*lst_columns))
        ]
        return cls(index=index, columns=columns)

    @classmethod
    def from_pandas(cls, df, index_names=None):
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
        keys = [key if isinstance(key, tuple) else (key,) for key in df.index.tolist()]
        index = [("index{}".format(i), cindex) for i, cindex in enumerate(zip(*keys))]
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
                columns = [
                    ("c{}".format(i), col) for i, col in enumerate(zip(*data.tolist()))
                ]
            else:
                raise TypeError
        else:
            raise TypeError
        return cls(index=index, columns=columns)

    @classmethod
    def _from_data_frame_ref(cls, df_ref):
        return cls(None, None, _impl=df_ref)

    # Aliases
    addColumn = add_column
    addRow = add_row
    fromDict = from_dict
    fromNumpy = from_numpy
    fromPandas = from_pandas
    getColumn = get_column
    getHeaders = get_headers
    getNumCols = get_num_cols
    getNumIndices = get_num_indices
    getNumRows = get_num_rows
    getRow = get_row
    getRowByIndex = get_row_by_index
    setColumn = set_column
    setValues = set_values
    toDict = to_dict
    toList = to_list
    toPandas = to_pandas
