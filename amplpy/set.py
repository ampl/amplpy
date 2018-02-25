# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring
from numbers import Real

from .entity import Entity
from .utils import Utils, Tuple
from .dataframe import DataFrame
from .iterators import MemberRangeIterator
try:
    import numpy as np
except ImportError:
    np = None


class Set(Entity):
    """
    Represents an AMPL set. In case of not indexed sets, this class exposes
    iterators for accessing its elements. The members of the set are tuples.
    All these methods throw a TypeError if called for an indexed set.

    In case of indexed sets, you can gain access to the instances using the
    operator [].

    All the accessors in this class throw an RuntimeError if the instance has
    been deleted in the underlying AMPL interpreter.

    Data can be assigned to the set using the methods
    :func:`~amplpy.Set.setValues` (for non-indexed sets only) or using
    :func:`~amplpy.AMPL.setData` and an object of class
    :class:`~amplpy.DataFrame`.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, Set)

    def instances(self):
        """
        Get an iterator to iterate over all the instances in a Set.
        """
        return Entity.instances(self)

    def arity(self):
        """
        The arity of the set, or number of components in each member of this
        set.
        """
        return int(self._impl.arity())

    def getValues(self):
        """
        Get values of this set in a DataFrame. Valid only for non-indexed sets.
        """
        return Entity.getValues(self)

    def members(self):
        """
        Get members (tuples) of this Set. Valid only for non-indexed sets.
        """
        # FIXME: _impl.members() is missing
        return MemberRangeIterator(self._impl.get().members(), self.size)

    def size(self):
        """
        Get the number of tuples in this set. Valid only for non-indexed sets.
        """
        return int(self._impl.size())

    def contains(self, t):
        """
        Check wether this set instance contains the specified Tuple.
        Valid only for non-indexed sets.

        Args:
            t: Tuple to be found.
        """
        return self._impl.contains(Tuple(t)._impl)

    def setValues(self, values):
        """
        Set the tuples in this set. Valid only for non-indexed sets.

        Args:
            values: A list of tuples or a :class:`~amplpy.DataFrame`.

        In the case of a :class:`~amplpy.DataFrame`, the number of indexing
        columns of the must be equal to the arity of the set. In the case of
        a list of tuples, the arity of each tuple must be equal to the arity
        of the set.

        For example, considering the following AMPL entities and corresponding
        Python objects:

        .. code-block:: ampl

            set A := 1..2;
            param p{i in A} := i+10;
            set AA;

        The following is valid:

        .. code-block:: python

            A, AA = ampl.getSet('A'), ampl.getSet('AA')
            AA.setValues(A.getValues())  # AA has now the members {1, 2}
        """
        if isinstance(values, (list, set)):
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                self._impl.setValuesStr(values, len(values))
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                self._impl.setValuesDbl(values, len(values))
            elif all(isinstance(value, tuple) for value in values):
                self._impl.setValues(Utils.toTupleArray(values), len(values))
            else:
                raise TypeError
        else:
            if np is not None and isinstance(values, np.ndarray):
                self.setValues(DataFrame.fromNumpy(values).toList())
                return
            Entity.setValues(self, values)
