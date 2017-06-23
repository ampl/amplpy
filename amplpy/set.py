from .entity import Entity
from .utils import Utils
from .dataframe import DataFrame
from .iterators import EntityIterator, MemberRangeIterator


class Set(Entity):
    """
    Represents an AMPL set. In case of not indexed sets, this class exposes
    iterators for accessing its elements. The members of the set are tuples.
    All these methods throw a LogicError if called for an indexed set.

    In case of indexed sets, you can gain access to the instances using the
    operator [].

    All the accessors in this class throw an RunTimeError if the instance has
    been deleted in the underlying AMPL interpreter.

    Data can be assigned to the set using the methods
    :func:`~amplpy.Set.setValues` (for non-indexed sets only) or using
    :func:`~amplpy.AMPL.setData` and an object of class
    :class:`~amplpy.DataFrame`.
    """

    def __init__(self, *args, **kwargs):
        _impl = kwargs.get('_impl', None)
        Entity.__init__(
            self,
            _impl,
            lambda it: MemberRangeIterator(it.members())
        )

    def __len__(self):
        return self.size()

    def instances(self):
        """
        Get an iterator to iterate over all the instances in a Set.
        """
        # return EntityIterator(self._impl.instances(), Set)
        raise NotImplementedError

    def arity(self):
        """
        The arity of s, or number of components in each member of this set.
        """
        return self._impl.arity()

    def getValues(self):
        """
        Get values of this set in a DataFrame. Valid only for non-indexed sets.
        """
        raise NotImplementedError

    def members(self):
        """
        Get members (tuples) of this Set. Valid only for non-indexed sets.
        """
        # return self._impl.members()
        raise NotImplementedError

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
        raise NotImplementedError

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
            AA.setValues(A.getValues())  # A has now the members {1, 2}
        """
        if isinstance(values, (list, set)):
            pass
        if isinstance(values, DataFrame):
            pass
        else:
            raise TypeError
        raise NotImplementedError

    def getValues(self):
        """
        Get all the tuples in this set instance in a DataFrame.
        """
        raise NotImplementedError

    @classmethod
    def fromSetRef(cls, setRef):
        return cls(_impl=setRef)
