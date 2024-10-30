# -*- coding: utf-8 -*-
from numbers import Real
from collections.abc import Iterable


try:
    import numpy as np
except ImportError:
    np = None


cdef class Set(Entity):
    """
    Represents an AMPL set. In case of not indexed sets, this class exposes
    iterators for accessing its elements. The members of the set are tuples.
    All these methods throw a TypeError if called for an indexed set.

    In case of indexed sets, you can gain access to the instances using the
    operator [].

    All the accessors in this class throw an RuntimeError if the instance has
    been deleted in the underlying AMPL interpreter.

    Data can be assigned to the set using the methods
    :func:`~amplpy.Set.set_values`
    (for non-indexed sets only) or using
    :func:`~amplpy.AMPL.set_data`
    and an object of class
    :class:`~amplpy.DataFrame`.
    """
    @staticmethod
    cdef create(campl.AMPL* ampl_c, char* name, campl.AMPL_TUPLE* index, parent):
        entity = Set()
        entity._c_ampl = ampl_c
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_SET
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def __setitem__(self, index, value):
        self.__getitem__(index).set_values(value)

    def __iter__(self):
        if self.is_scalar():
            return self.members()
        else:
            return self.instances()

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
        cdef size_t arity
        PY_AMPL_CALL(campl.AMPL_SetGetArity(self._c_ampl, self._name, &arity))
        return int(arity)

    def get_values(self):
        """
        Get values of this set in a DataFrame. Valid only for non-indexed sets.
        """
        cdef campl.AMPL_DATAFRAME* df_c
        campl.AMPL_SetInstanceGetValuesDataframe(self._c_ampl, self._name, self._index, &df_c)
        return DataFrame.create(df_c)

    def members(self):
        """
        Get members (tuples) of this Set. Valid only for non-indexed sets.
        """
        return MemberRangeIterator.create(self._c_ampl, self._name, self._index, self)

    def size(self):
        """
        Get the number of tuples in this set. Valid only for non-indexed sets.
        """
        cdef size_t size
        PY_AMPL_CALL(campl.AMPL_SetInstanceGetSize(self._c_ampl, self._name, self._index, &size))
        return int(size)

    def contains(self, t):
        """
        Check wether this set instance contains the specified Tuple.
        Valid only for non-indexed sets.

        Args:
            t: Tuple to be found.
        """
        cdef bool_c contains_c
        cdef campl.AMPL_TUPLE* t_c = to_c_tuple(t)
        campl.AMPL_SetInstanceContains(self._c_ampl, self._name, NULL, t_c, &contains_c)    
        campl.AMPL_TupleFree(&t_c)
        return contains_c

    def set_values(self, values):
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

            A, AA = ampl.get_set('A'), ampl.get_set('AA')
            AA.set_values(A.get_values())  # AA has now the members {1, 2}
        """
        cdef DataFrame df = None
        if not self.is_scalar():
            if not isinstance(values, dict):
                raise TypeError("Excepted dictionary of set members for each index.")
            for index, members in values.items():
                self[index].set_values(members)
        elif isinstance(values, DataFrame):
            df = values
            PY_AMPL_CALL(campl.AMPL_SetInstanceSetValuesDataframe(self._c_ampl, self._name, self._index, df.get_ptr()))
        elif isinstance(values, Iterable):
            dimen = self.arity()
            if dimen == 1 and all(isinstance(value, str) for value in values):
                if not isinstance(values, (list, tuple)):
                    values = list(values)
                setValues(self._c_ampl, self._name, self._index, values, len(values))
            elif dimen == 1 and all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                setValues(self._c_ampl, self._name, self._index, values, len(values))
            else:

                def cast_value(value):
                    if isinstance(value, str):
                        return value
                    elif isinstance(value, Real):
                        return float(value)
                    else:
                        raise TypeError("Excepted string or real.")

                def cast_row(row):
                    if isinstance(row, str):
                        return row
                    elif isinstance(row, Real):
                        return float(row)
                    elif isinstance(row, Iterable):
                        return tuple(map(cast_value, row))
                    else:
                        if dimen == 1:
                            raise TypeError("Excepted string or real.")
                        else:
                            raise ValueError(f"Excepted tuple of arity {dimen}.")

                values = [cast_row(row) for row in values]
                if dimen == 1:
                    if any(isinstance(row, tuple) for row in values):
                        raise ValueError(
                            f"Trying to assign tuples to set of arity {dimen}."
                        )
                else:
                    if any(
                        not isinstance(row, tuple) or len(row) != dimen
                        for row in values
                    ):
                        raise ValueError(f"Expected tuples of arity {dimen}.")
                setValues(self._c_ampl, self._name, self._index, values, len(values))
        else:
            Entity.set_values(self, values)

    # Aliases
    getValues = get_values
    setValues = set_values
