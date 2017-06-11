import amplpython
from base import BaseClass


class Tuple(BaseClass):
    def __init__(self, *args, **kwargs):
        if len(args) != 0:
            va = Utils.toVariantArray(list(args))
            self._impl = amplpython.Tuple.Factory(va, len(args))
        else:
            self._impl = kwargs.get('_impl', None)

    def toTuple(self):
        return tuple(
            Utils.castVariant(self._impl.getIndex(i))
            for i in range(self._impl.size())
        )

    def toPyObj(self):
        size = self._impl.size()
        if size == 1:
            return Utils.castVariant(self._impl.getIndex(0))
        else:
            return tuple(
                Utils.castVariant(self._impl.getIndex(i))
                for i in range(size)
            )

    @classmethod
    def fromTupleRef(cls, tupleRef):
        return cls(_impl=amplpython.Tuple.Factory(tupleRef))


class Utils:
    @staticmethod
    def toVariantArray(list):
        va = amplpython.VariantArray(len(list))
        for i in xrange(len(list)):
            va[i] = amplpython.Variant(list[i])
        return va

    @staticmethod
    def castVariant(variant):
        if variant.type() == amplpython.NUMERIC:
            return variant.dbl()
        elif variant.type() == amplpython.STRING:
            return variant.str()

    @staticmethod
    def castVariantRef(variantref):
        return Utils.castVariant(amplpython.Variant(variantref))

    @staticmethod
    def castToList(value):
        if isinstance(value, (list, tuple)):
            return list(value)
        else:
            return [value]

    @staticmethod
    def castToTuple(value):
        if isinstance(value, (list, tuple)):
            return tuple(value)
        else:
            return tuple([value])


def multidict(d):
    try:
        ncols = min(len(d[k]) for k in d)
    except TypeError:
        raise TypeError
    return [list(d.keys())] + [{k: d[k][i] for k in d} for i in range(ncols)]
