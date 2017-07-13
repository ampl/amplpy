# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from . import amplpython
from .base import BaseClass


def lock_call(call, lock):
    lock.acquire()
    try:
        result = call()
    except Exception:
        lock.release()
        raise
    else:
        lock.release()
        return result


class Tuple(BaseClass):
    def __init__(self, values=None, **kwargs):
        if values is not None:
            values = Utils.convToList(values)
            va = Utils.toVariantArray(values)
            self._impl = amplpython.Tuple.Factory(va, len(values))
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
            return self.toTuple()

    @classmethod
    def fromTupleRef(cls, tupleRef):
        return cls(_impl=amplpython.Tuple.Factory(tupleRef))


class Utils(object):
    @staticmethod
    def toVariantArray(lst):
        va = amplpython.VariantArray(len(lst))
        for i in range(len(lst)):
            va[i] = amplpython.Variant(lst[i])
        return va

    @staticmethod
    def toTupleArray(lst):
        ta = amplpython.TupleArray(len(lst))
        for i in range(len(lst)):
            ta[i] = Tuple(lst[i])._impl
        return ta

    @staticmethod
    def castVariant(variant):
        if variant.type() == amplpython.NUMERIC:
            return variant.dbl()
        elif variant.type() == amplpython.STRING:
            return variant.str()

    @staticmethod
    def castStringArray(sarray):
        return [sarray.getIndex(i) for i in range(sarray.size())]

    @staticmethod
    def castVariantRef(variantref):
        return Utils.castVariant(amplpython.Variant(variantref))

    @staticmethod
    def convToList(value):
        if isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return list(value)
        else:
            return [value]


def multidict(d):
    try:
        ncols = min(len(d[k]) for k in d)
    except TypeError:
        raise TypeError
    return [list(d.keys())] + [{k: d[k][i] for k in d} for i in range(ncols)]
