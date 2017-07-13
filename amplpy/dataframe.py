# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from .base import BaseClass
from .utils import Utils, Tuple
from .iterators import RowIterator, ColIterator
from . import amplpython


class Row(BaseClass):
    """
    Represents a row in a :class:`~amplpy.DataFrame`.
    """

    def __init__(self, _impl):
        self._impl = _impl

    def __iter__(self):
        return RowIterator(self._impl)

    def __getitem__(self, key):
        return Utils.castVariantRef(self._impl.getIndex(key))

    def toString(self):
        return str(list(self))


class Column(BaseClass):
    """
    Represents a column in a :class:`~amplpy.DataFrame`.
    """

    def __init__(self, _impl):
        self._impl = _impl

    def __iter__(self):
        return ColIterator(self._impl)

    def toString(self):
        return str(list(self))


class DataFrame(BaseClass):
    """
    A DataFrame object, used to communicate data to and from the AMPL entities.

    An object of this class can be used to do the following tasks:
    - Assign values to AMPL entities (once the DataFrame is populated, use
    :func:`~amplpy.AMPL.setData` to assign its values to the modelling entities
    in its columns)
    - Get values from AMPL, decoupling the values from the AMPL entities they
    originate via :func:`~amplpy.Entity.getValues`.

    A DataFrame object can be created in various ways.

    - Create a skeleton by specifiying manually the indexing columns and the
      column headers.
    - Get values from AMPL, decoupling the values from the AMPL entities they
      originate from (via :func:`~amplpy.Entity.getValues`).

    Populating a DataFrame object can be done adding row by row to a
    pre-existing skeleton via :func:`~amplpy.DataFrame.addRow`, setting whole
    columns of a pre-existing skeleton via :func:`~amplpy.DataFrame.setColumn`
    or adding columns (including indexing columns) via
    :func:`~amplpy.DataFrame.addColumn`.

    Modifying a DataFrame object can be done via
    :func:`~amplpy.DataFrame.setColumn` or, item by item, via
    :func:`~amplpy.DataFrame.setValue`.

    Accessing data in a DataFrame can be done row by row using
    :func:`~amplpy.DataFrame.getRow` or by column via
    :func:`~amplpy.DataFrame.getColumn`.
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
            self._impl = amplpython.DataFrame.factory(
                len(index),
                list(index) + list(columns),
                len(index) + len(columns)
            )
        else:
            self._impl = kwargs.get('_impl', None)

    def __iter__(self):
        # FIXME: C++ iterators for dataframes not working with SWIG.
        return (self.getRowByIndex(i) for i in range(self.getNumRows()))

    def getNumCols(self):
        """
        Get the total number of columns in this dataframe (indexarity + number
        of values).

        Returns:
            The number of columns.
        """
        return self._impl.getNumCols()

    def getNumRows(self):
        """
        Get the number of data rows in this dataframe.

        Returns:
            The number of rows.
        """
        return self._impl.getNumRows()

    def getNumIndices(self):
        """
        Get the number of indices (the indexarity) of this dataframe.

        Returns:
            The number of indices needed to access one row of this dataframe.
        """
        return self._impl.getNumIndices()

    def addRow(self, *value):
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
        assert len(value) == self.getNumCols()
        self._impl.addRow(Tuple(value)._impl)

    def addColumn(self, header, values=[]):
        """
        Add a new column with the corresponding header and values to the
        dataframe.

        Args:
            header: The name of the new column.

            values: A list of size :func:`~amplpy.DataFrame.getNumRows` with
            all the values of the new column.
        """
        if len(values) == 0:
            self._impl.addColumn(header)
        else:
            assert len(values) == self.getNumRows()
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                self._impl.addColumnStr(header, values)
            elif all(isinstance(value, (float, int)) for value in values):
                values = list(map(float, values))
                self._impl.addColumnDbl(header, values)
            else:
                raise NotImplementedError

    def getColumn(self, header):
        """
        Get the specified column as a view object.

        Args:
            header: The header of the column.
        """
        return Column(self._impl.getColumn(header))

    def setColumn(self, header, values):
        """
        Set the values of a column.

        Args:
            header: The header of the column to be set.

            values: The values to set.
        """
        if any(isinstance(value, basestring) for value in values):
            values = list(map(str, values))
            self._impl.setColumnStr(header, values, len(values))
        elif all(isinstance(value, (float, int)) for value in values):
            values = list(map(float, values))
            self._impl.setColumnDbl(header, values, len(values))
        else:
            raise NotImplementedError

    def getRow(self, key):
        """
        Get a row by value of the indexing columns. If the index is not
        specified, gets the only row of a dataframe with no indexing columns.

        Args:
            key: Tuple representing the index of the desired row.

        Returns:
            The row.
        """
        return Row(self._impl.getRow(Tuple(key)._impl))

    def getRowByIndex(self, index):
        """
        Get row by numeric index.

        Args:
            index: Zero-based index of the row to get.

        Returns:
            The corresponding row.
        """
        assert isinstance(index, int)
        return Row(self._impl.getRowByIndex(index))

    def getHeaders(self):
        """
         Get the headers of this DataFrame.

         Returns:
            The headers of this DataFrame.
        """
        headers = self._impl.getHeaders()
        return tuple(headers.getIndex(i) for i in range(headers.size()))

    def setValues(self, values):
        """
        Set the values of a DataFrame from a dictionary.

        Args:
            values: Dictionary with the values to set.
        """
        ncols = self.getNumCols()
        nindices = self.getNumIndices()
        for key, value in values.items():
            key = Utils.convToList(key)
            assert len(key) == nindices
            value = Utils.convToList(value)
            assert len(value) == ncols-nindices
            self.addRow(key + value)

    def toDict(self):
        d = {}
        nindices = self.getNumIndices()
        for i in range(self.getNumRows()):
            row = list(self.getRowByIndex(i))
            if nindices > 1:
                key = tuple(row[:nindices])
            else:
                key = row[0]
            d[key] = row[nindices:]
        return d

    def toList(self):
        return [tuple(self.getRowByIndex(i)) for i in range(self.getNumRows())]

    @classmethod
    def _fromDataFrameRef(cls, dfRef):
        return cls(None, None, _impl=dfRef)
