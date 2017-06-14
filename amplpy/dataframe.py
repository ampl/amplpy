from .base import BaseClass
from .utils import Utils, Tuple
from .iterators import RowIterator, ColIterator
from . import amplpython


class Row(BaseClass):
    def __init__(self, **kwargs):
        self._impl = kwargs.get('_impl', None)

    def __iter__(self):
        return RowIterator(self._impl)

    def toString(self):
        return str(list(self))

    @classmethod
    def fromRowRef(cls, rRef):
        return cls(_impl=rRef)


class Column(BaseClass):
    def __init__(self, **kwargs):
        self._impl = kwargs.get('_impl', None)

    def __iter__(self):
        return ColIterator(self._impl)

    def toString(self):
        return str(list(self))

    @classmethod
    def fromColumnRef(cls, cRef):
        return cls(_impl=cRef)


class DataFrame(BaseClass):
    """
    A DataFrame object, used to communicate data to and from the AMPL entities.
    """

    def __init__(self, index, columns, **kwargs):
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

    def setValues(self, values):
        ncols = self.getNumCols()
        nindices = self.getNumIndices()
        for key, value in values.items():
            key = Utils.castToList(key)
            assert len(key) == nindices
            value = Utils.castToList(value)
            assert len(value) == ncols-nindices
            self.addRow(key + value)

    def addRow(self, value):
        assert len(value) == self.getNumCols()
        self._impl.addRow(Tuple(*value)._impl)

    def addColumn(self, header, values=[]):
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
        return Column.fromColumnRef(self._impl.getColumn(header))

    def getRow(self, key):
        key = Utils.castToList(key)
        return Row.fromRowRef(self._impl.getRow(Tuple(*key)._impl))

    def getRowByIndex(self, index):
        assert isinstance(index, int)
        return Row.fromRowRef(self._impl.getRowByIndex(index))

    def getNumCols(self):
        return self._impl.getNumCols()

    def getNumRows(self):
        return self._impl.getNumRows()

    def getNumIndices(self):
        return self._impl.getNumIndices()

    def getHeaders(self):
        headers = self._impl.getHeaders()
        return tuple(headers.getIndex(i) for i in range(headers.size()))

    @classmethod
    def fromDataFrameRef(cls, dfRef):
        return cls(None, None, _impl=dfRef)
