# -*- coding: utf-8 -*-

from libc.string cimport strdup


try:
    import pandas as pd
except ImportError:
    pd = None


cdef class Entity(object):
    """
    An AMPL entity such as a parameter or a variable.

    An entity can either represent a single instance of an AMPL algebraic
    entity or, if the corresponding declaration has an indexing expression, a
    mapping from keys to instances. In the derived classes, it has methods to
    access instance-level properties which can be used in case the represented
    entity is scalar.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), use the function
    :func:`~amplpy.Entity.get_values`.

    The algebraic entities which currently have an equivalent class in the API
    are:

    - Variables (see :class:`~amplpy.Variable`)
    - Constraints (see :class:`~amplpy.Constraint`)
    - Objectives (see :class:`~amplpy.Objective`)
    - Sets (see :class:`~amplpy.Set`)
    - Parameters (see :class:`~amplpy.Parameter`)
    """
    cdef campl.AMPL* _c_ampl
    cdef str _name
    cdef campl.AMPL_TUPLE* _index
    cdef campl.AMPL_ENTITYTYPE wrap_function

    @staticmethod
    cdef create(campl.AMPL* ampl_c, name, campl.AMPL_TUPLE* index):
        cdef campl.AMPL_ENTITYTYPE entitytype
        PY_AMPL_CALL(campl.AMPL_EntityGetType(ampl_c, name.encode('utf-8'), &entitytype))
        entity = Entity()
        entity._c_ampl = ampl_c
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_UNDEFINED
        return entity

    #def __dealloc__(self):
    #    if self._index is not NULL:
    #        campl.AMPL_TupleFree(&self._index)

    def to_string(self):
        cdef char* output_c
        campl.AMPL_EntityGetDeclaration(self._c_ampl, self._name.encode('utf-8'), &output_c)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)
        return output

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        assert self.wrap_function is not None
        return InstanceIterator.create(self._c_ampl, self._name, self.wrap_function)

    def __getitem__(self, index):
        if not isinstance(index, (tuple, list)):
            index = [index]
        cdef campl.AMPL_TUPLE* tuple_c =  to_c_tuple(index)
        return create_entity(self.wrap_function, self._c_ampl, self._name, tuple_c)

    def get(self, *index):
        """
        Get the instance with the specified index.

        Returns:
            The corresponding instance.
        """
        assert self.wrap_function is not None
        cdef campl.AMPL_TUPLE* tuple_c
        cdef char* name_c
        if len(index) == 1 and isinstance(index[0], (tuple, list)):
            index = index[0]
            index = list(index)
        if len(index) == 0:
            return create_entity(self.wrap_function, self._c_ampl, self._name, NULL)
        else:
            tuple_c =  to_c_tuple(index)
            if self.wrap_function == campl.AMPL_PARAMETER:
                campl.AMPL_InstanceGetName(self._c_ampl, self._name.encode('utf-8'), tuple_c, &name_c)
                entity = create_entity(self.wrap_function, self._c_ampl, name_c.decode('utf-8'), NULL).value()
                campl.AMPL_StringFree(&name_c)
                return entity
            else:
                return create_entity(self.wrap_function, self._c_ampl, self._name, tuple_c)

    def find(self, index):
        """
        Searches the current entity for an instance with the specified index.

        Returns:
            The wanted instance if found, otherwise it returns `None`.
        """
        assert self.wrap_function is not None
        cdef campl.AMPL_TUPLE* index_c = to_c_tuple(index)
        cdef campl.AMPL_TUPLE** indices_c
        cdef size_t size
        campl.AMPL_EntityGetTuples(self._c_ampl, self._name.encode('utf-8'), &indices_c, &size)
        for i in range(size):
            if campl.AMPL_TupleCompare(index_c, indices_c[i]) == 0:
                free(indices_c)
                return create_entity(self.wrap_function, self._c_ampl, self._name, index_c)
        free(indices_c)
        return None

    def instances(self):
        """
        Get all the instances in this entity.
        """
        return InstanceIterator.create(self._c_ampl, self._name, self.wrap_function)

    def name(self):
        """
        Get the name of this entity.
        """
        return self._name

    def indexarity(self):
        """
        Get the indexarity of this entity (sum of the dimensions of the
        indexing sets).
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
        cdef size_t indexarity
        if self._index is not NULL:
            indexarity = 0
        else:
            campl.AMPL_EntityGetIndexarity(self._c_ampl, self._name.encode('utf-8'), &indexarity)
        return indexarity

    def is_scalar(self):
        """
        Check whether this entity is scalar. Equivalent to testing whether
        :func:`~amplpy.Entity.indexarity` is equal to zero.

        Returns:
            True if the entity is scalar (not indexed over any set).
        """
        try:
            return self.indexarity() == 0
        except:
            return True

    def num_instances(self):
        """
        Get the number of instances in this entity.
        """
        cdef size_t size
        campl.AMPL_EntityGetNumInstances(self._c_ampl, self._name.encode('utf-8'), &size);
        return int(size)

    def get_indexing_sets(self):
        """
        Get the AMPL string representation of the sets on which this entity is
        indexed. The obtained vector can be modified without any effect to the
        entity.

        Returns:
            The string representation of the indexing sets for this entity or
            an empty array if the entity is scalar.
        """
        cdef size_t i
        cdef size_t size
        cdef char** sets
        cdef list pylist = []
        campl.AMPL_EntityGetIndexingSets(self._c_ampl, self._name.encode('utf-8'), &sets, &size)
        for i in range(size):
            if sets[i] != NULL:
                pylist.append(sets[i].decode('utf-8'))
            else:
                pylist.append(None)
            campl.AMPL_StringFree(&sets[i])
        free(sets)
        
        return pylist

    def xref(self):
        """
        Get the names of all entities which depend on this one.

        Returns:
            A list with the names of all entities which depend on this one.
        """
        cdef size_t size
        cdef char** xref
        cdef list pylist = []
        campl.AMPL_EntityGetXref(self._c_ampl, self._name.encode('utf-8'), &xref, &size)
        for i in range(size):
            if xref[i] != NULL:
                pylist.append(xref[i].decode('utf-8'))
                campl.AMPL_StringFree(&xref[i])
            else:
                pylist.append(None)
        free(xref)
        return pylist

    def get_values(self, suffixes=None):
        """
        If a list of suffixes is provided, get the specified suffixes value for
        all instances. Otherwise, get all the principal values of this entity.
        The specific returned value depends on the type of entity (see list
        below). For:

        - Variables and Objectives it returns the suffix ``val``.
        - Parameters it returns their values.
        - Constraints it returns the suffix ``dual``.
        - Sets it returns all the members of the set. Note that it does not
          apply to indexed sets. See :func:`~amplpy.Set.get_values`.

        Raises:
            RuntimeError: if there are issues with the data.

        Retruns:
            A :class:`~amplpy.DataFrame` containing the values for all
            instances.
        """
        cdef campl.AMPL_DATAFRAME* df_c
        cdef char** suffixes_c
        cdef size_t n
        if suffixes is None:
            n = 0
            PY_AMPL_CALL(campl.AMPL_EntityGetValues(self._c_ampl, self._name.encode('utf-8'), NULL, n, &df_c))
        else:
            if isinstance(suffixes, str):
                suffixes = [suffixes]
            else:
                suffixes = list(map(str, suffixes))
            suffixes_c = <char**> malloc(len(suffixes) * sizeof(char*))
            for i in range(len(suffixes)):
                suffixes_c[i] = strdup(suffixes[i].encode('utf-8'))
            n = len(suffixes)
            campl.AMPL_EntityGetValues(self._c_ampl, self._name.encode('utf-8'), suffixes_c, n, &df_c)
            for i in range(len(suffixes)):
                free(suffixes_c[i])
            free(suffixes_c)

        return DataFrame.create(df_c)

    def to_pandas(self, **kwargs):
        """
        Equivalent to ``Entity.get_values().``:func:`~amplpy.DataFrame.to_pandas`.
        """
        return self.get_values().to_pandas(**kwargs)

    def to_dict(self, **kwargs):
        """
        Equivalent to ``Entity.get_values().``:func:`~amplpy.DataFrame.to_dict`.
        """
        return self.get_values().to_dict(**kwargs)

    def to_list(self, **kwargs):
        """
        Equivalent to ``Entity.get_values().``:func:`~amplpy.DataFrame.to_list`.
        """
        return self.get_values().to_list(**kwargs)

    def set_values(self, data):
        """
        Set the values of this entiy to the correponding values of a
        DataFrame indexed over the same sets (or a subset).
        This function assigns the values in the first data column of
        the passed dataframe to the entity the function is called from.
        In particular, the statement:

        .. code-block:: python

            x.set_values(y.get_values())

        is semantically equivalent to the AMPL statement:

        .. code-block:: ampl

            let {s in S} x[s] := y[s];

        Args:
            data: The data to set the entity to.
        """
        cdef DataFrame df
        cdef campl.AMPL_DATAFRAME* df_c 
        cdef char* _name_c 
        campl.AMPL_InstanceGetName(self._c_ampl, self._name.encode('utf-8'), self._index, &_name_c)
        if isinstance(data, DataFrame):
            df = data
            df_c = df.get_ptr()
            campl.AMPL_EntitySetValues(self._c_ampl, _name_c, df_c)
            campl.AMPL_StringFree(&_name_c)
        elif isinstance(data, dict):
            df = DataFrame.from_dict(data)
            df_c = df.get_ptr()
            campl.AMPL_EntitySetValues(self._c_ampl, _name_c, df_c)
            campl.AMPL_StringFree(&_name_c)
        else:
            if pd is not None and isinstance(data, (pd.DataFrame, pd.Series)):
                df = DataFrame.from_pandas(data, indexarity=self.indexarity())
                df_c = df.get_ptr()
                campl.AMPL_EntitySetValues(self._c_ampl, _name_c, df_c)
                campl.AMPL_StringFree(&_name_c)
                return
            raise TypeError(f"Unexpected data type: {type(data)}.")

    # Aliases
    toString = to_string
    getIndexingSets = get_indexing_sets
    getValues = get_values
    isScalar = is_scalar
    numInstances = num_instances
    setValues = set_values
