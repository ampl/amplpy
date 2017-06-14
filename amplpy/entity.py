from .base import BaseClass
from .utils import Tuple
from .iterators import EntityIterator


class Entity(BaseClass):
    """
    An AMPL entity such as a parameter or a variable.

    An entity can either represent a single instance of an AMPL algebraic
    entity or, if the corresponding declaration has an indexing expression, a
    mapping from keys to instances. In the derived classes, it has methods to
    access instance-level properties which can be used in case the represented
    entity is scalar.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), use the function
    :func:`~amplpy.Entity.getValues`.

    The algebraic entities which currenty have an equivalent class in the API
    are:

    - Variables (see :class:`~amplpy.Variable`)
    - Constraints (see :class:`~amplpy.Constraint`)
    - Objectives (see :class:`~amplpy.Objective`)
    - Sets (see :class:`~amplpy.Set`)
    - Parameters (see :class:`~amplpy.Parameter`)
    """

    def __init__(self, _impl, wrapFunction=None):
        BaseClass.__init__(self, _impl)
        self.wrapFunction = wrapFunction

    def __iter__(self):
        assert self.wrapFunction is not None
        return EntityIterator(self._impl, self.wrapFunction)

    def __getitem__(self, *key):
        assert self.wrapFunction is not None
        if len(key) == 1 and isinstance(key, (tuple, list)):
            key = key[0]
        return self.wrapFunction(self.get(key))

    def get(self, index=None):
        assert self.wrapFunction is not None
        indexarity = self._impl.indexarity()
        if index is None:
            assert indexarity == 0
            return self.wrapFunction(self._impl.get())
        else:
            if not isinstance(index, (tuple, list)):
                index = (index,)
            assert indexarity == len(index)
            return self.wrapFunction(self._impl.get(Tuple(*index)._impl))

    def indexarity(self):
        """
        Get the indexarity of this entity (sum of the dimensions of the indexing
        sets).
        This value indicates the arity of the tuple to be passed to the method
        :func:`~amplpy.Entity.get` in order to access an instance of this
        entity. See the following AMPL examples:

        .. code-block:: ampl

            var x;               # indexarity = 0
            var y {1..2};        # indexarity = 1
            var z {1..2,3..4};   # indexarity = 2
            var zz {{(1, 2)}};   # indexarity = 2

        Returns:
            The sum of the dimensions of the indexing sets or 0 if the
            entity is not indexed.
        """
        return self._impl.indexarity()

    def isScalar(self):
        """
        Check whether this entity is scalar. Equivalent to testing whether
        :func:`~amplpy.Entity.indexarity` is equal to zero.

        Returns:
            True if the entity is scalar (not indexed over any set).
        """
        return self._impl.isScalar()

    def numInstances(self):
        """
        Get the number of instances in this entity.
        """
        return self._impl.numInstances()

    def getIndexingSets(self):
        """
        Get the AMPL string representation of the sets on which this entity is
        indexed. The obtained vector can be modified without any effect to the
        entity.

        Returns:
            The string representation of the indexing sets for this entity or
            an empty array if the entity is scalar.
        """
        # return self._impl.getIndexingSets()
        raise NotImplementedError

    def getValues(self, suffixes=None):
        """
        If a list of suffixes is provided, get the specified suffixes value for
        all instances. Otherwise, get all the principal values of this entity.
        The specific returned value depends on the type of entity (see list
        below). For:

        - Variables and Objectives it returns the suffix ``val``.
        - Parameters it returns their values.
        - Constraints it returns the suffix ``dual``.
        - Sets it returns all the members of the set. Note that it does not
          apply to indexed sets. See :func:`~amplpy.Set.getValues`.

        Retruns:
            A :class:`~amplpy.DataFrame` containing the values for all instances.
        """
        if suffixes is None:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def setValues(self, data):
        """
        Set the values of this entiy to the correponding values of a
        DataFrame indexed over the same sets (or a subset).
        This function assigns the values in the first data column of
        the passed dataframe to the entity the function is called from.
        In particular, the statement:

        .. code-block:: python

            x.setValues(y.getValues())

        is semantically equivalent to the AMPL statement:

        .. code-block:: ampl

            let {s in S} x[s] := y[s];

        Args:
            data: The data to set the entity to.
        """
        raise NotImplementedError
