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
    cdef AMPL _ampl
    cdef char* _name
    cdef campl.AMPL_TUPLE* _index
    cdef campl.AMPL_ENTITYTYPE wrap_function
    cdef object _entity

    @staticmethod
    cdef create(AMPL ampl, char *name, campl.AMPL_TUPLE* index, object parent):
        entity = Entity()
        entity._ampl = ampl
        Py_INCREF(entity._ampl)
        entity._name = name
        entity._index = index
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        errorinfo = campl.AMPL_EntityGetType(entity._ampl._c_ampl, name, &entitytype)
        if errorinfo:
            #free(name)
            PY_AMPL_CALL(errorinfo)
        entity.wrap_function = entitytype
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def __dealloc__(self):
        if self._entity is not None:
            Py_DECREF(self._entity)
        if self._index is not NULL:
            campl.AMPL_TupleFree(&self._index)
        else:
            campl.AMPL_StringFree(&self._name)
        Py_DECREF(self._ampl)

    cdef _check_scalar(self):
        """
        Raise TypeError if this object represents an indexed entity rather than
        a scalar entity or a single instance. Instance-level accessors must not
        be forwarded to the native layer for indexed entities: for a
        single-instance family the interpreter returns the indexing key in
        place of the suffix value, which would otherwise be reported as a
        meaningless number or string.

        The result is not cached: the entity can be redeclared with a
        different indexing (e.g., after reset() or delete) while this
        object exists.
        """
        if self._is_instance():
            return
        self._raise_if_indexed(False)

    cdef _check_empty_index(self):
        """
        Raise TypeError for an empty index (e.g., y[()]) on an indexed entity.
        An empty index names the bare entity, which AMPL accepts: for an
        indexed entity with a single instance it evaluates to the index of
        that instance instead of failing. On a scalar entity, x[()] is valid
        and names the entity itself.
        """
        self._raise_if_indexed(True)

    cdef _raise_if_indexed(self, bint empty_index):
        """
        Shared by _check_scalar() and _check_empty_index(): raise TypeError if
        the entity is indexed, with advice that suits the entity type.
        """
        cdef size_t indexarity = self._family_indexarity()
        if indexarity == 0:
            return
        name = self._name.decode('utf-8')
        if empty_index:
            raise TypeError(
                f"'{name}' is an indexed entity (indexarity {indexarity}); an "
                f"empty index is only valid for a scalar entity. Pass the "
                f"index of an instance (e.g., {name}[...])."
            )
        if self.wrap_function == campl.AMPL_PARAMETER:
            # p[...] is the value of an instance, not an instance object.
            example = f"{name}[...] to read or {name}[...] = value to assign"
            bulk = "Use get_values() or set_values() to access all instances."
        elif self.wrap_function == campl.AMPL_SET:
            # Set.get_values() is itself an instance-level accessor.
            example = f"{name}[...]"
            bulk = "Use instances() to iterate over all instances."
        else:
            example = f"{name}[...]"
            bulk = "Use get_values() to access all instances."
        raise TypeError(
            f"'{name}' is an indexed entity; this method can only be used "
            f"on a scalar entity or on a single instance "
            f"(e.g., {example}). {bulk}"
        )

    cdef bint _is_instance(self) except -1:
        """
        True if this object is a single instance. An empty tuple (e.g., from
        x[()] on a scalar entity) names the bare entity, like no tuple at all:
        if the entity is later redeclared as indexed, such an object
        represents the whole family.
        """
        return not _is_empty_index(self._index)

    cdef _get_double_suffix(self, campl.AMPL_NUMERICSUFFIX suffix):
        """Read a numeric suffix of this scalar entity or instance."""
        cdef double value
        self._check_scalar()
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, suffix, &value))
        return value

    cdef _get_int_suffix(self, campl.AMPL_NUMERICSUFFIX suffix):
        """Read an integer suffix of this scalar entity or instance."""
        cdef int value
        self._check_scalar()
        PY_AMPL_CALL(campl.AMPL_InstanceGetIntSuffix(self._ampl._c_ampl, self._name, self._index, suffix, &value))
        return value

    cdef _get_string_suffix(self, campl.AMPL_STRINGSUFFIX suffix, bint check=True):
        """
        Read a string suffix of this scalar entity or instance. Pass
        check=False only if the caller has already checked that this object
        is not an indexed entity.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        if check:
            self._check_scalar()
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, suffix, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        try:
            return str(value_c.decode('utf-8'))
        finally:
            campl.AMPL_StringFree(&value_c)

    def to_string(self):
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* output_c
        errorinfo = campl.AMPL_EntityGetDeclaration(self._ampl._c_ampl, self._name, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)

        return output

    def set_suffix(self, suffix, value):
        """
        Set the value of a suffix for this entity or instance.

        For scalar or per-instance assignment pass a numeric or string value;
        the call is forwarded to the appropriate instance-level C API function.
        For bulk assignment over an indexed entity pass a
        :class:`pandas.DataFrame` or :class:`pandas.Series`.

        Args:
            suffix: Name of the suffix (e.g. ``"relax"``).

            value: Numeric value, string value, or a
            :class:`pandas.DataFrame` / :class:`pandas.Series` mapping
            indices to values.

        Raises:
            ValueError: if the number of index columns of the data does not
            match the indexarity of the entity, or if a DataFrame with rows
            is given for a scalar entity (pass a single value instead).
            TypeError: if a numeric or string value is passed for an indexed
            variable, constraint or objective.
        """
        cdef DataFrame df_typed
        cdef size_t indexarity
        if pd is not None and isinstance(value, (pd.Series, pd.DataFrame)):
            # The suffixes are assigned to the whole entity (by its name),
            # also when called on an instance.
            indexarity = self._family_indexarity()
            if isinstance(value, pd.Series):
                value = value.to_frame(name=suffix)
            df_typed = DataFrame.from_pandas(value, indexarity=indexarity)
        elif isinstance(value, DataFrame):
            df_typed = value
            indexarity = self._family_indexarity()
        elif isinstance(value, str):
            self._check_suffix_target()
            PY_AMPL_CALL(campl.AMPL_InstanceSetStringSuffix(self._ampl._c_ampl, self._name, self._index, suffix.encode('utf-8'), value.encode('utf-8')))
            return
        else:
            self._check_suffix_target()
            PY_AMPL_CALL(campl.AMPL_InstanceSetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, suffix.encode('utf-8'), float(value)))
            return
        if not self._has_rows_to_assign(df_typed, indexarity, self.name()):
            return
        if indexarity == 0:
            # Without index columns, AMPL_EntitySetSuffixes emits
            # "let name := value", which assigns the value of the entity
            # instead of the suffix.
            raise ValueError(
                f"'{self.name()}' is not indexed: pass a single numeric or "
                "string value to set_suffix() instead of a DataFrame."
            )
        PY_AMPL_CALL(campl.AMPL_EntitySetSuffixes(self._ampl._c_ampl, self._name, df_typed.get_ptr()))

    cdef size_t _family_indexarity(self) except? 0:
        """Indexarity of the entity, also when this object is an instance."""
        cdef size_t indexarity
        PY_AMPL_CALL(campl.AMPL_EntityGetIndexarity(self._ampl._c_ampl, self._name, &indexarity))
        return indexarity

    cdef bint _has_rows_to_assign(self, DataFrame df, size_t indexarity, str target) except -1:
        """
        Shared check for the bulk assignments (set_values() and set_suffix())
        before the data is sent to AMPL.

        The number of index columns of df must match the indexarity of the
        target, whether or not df has rows, so that the error does not depend
        on the data being empty. Returns False if df has no rows: assigning
        zero rows assigns nothing (each row becomes one ``let`` statement, so
        existing values are kept), and an empty statement must not be sent
        to the interpreter.
        """
        nindices = df._get_num_indices()
        if nindices != indexarity:
            raise ValueError(
                f"The data has {nindices} index column(s), but '{target}' "
                f"is indexed over {indexarity}."
            )
        return df._get_num_rows() != 0

    cdef _check_suffix_target(self):
        """
        Check that a single suffix value can be set on this object. Only
        variables, constraints and objectives have suffixes. For the other
        entity types (parameters, sets, tables and problems), AMPL reports
        that they have none (ValueError), whether they are indexed or not.
        """
        if (self.wrap_function == campl.AMPL_VARIABLE
                or self.wrap_function == campl.AMPL_CONSTRAINT
                or self.wrap_function == campl.AMPL_OBJECTIVE):
            self._check_scalar()

    def expand(self):
        """
        Get the expand message for this entity or instance.

        Returns:
            A string with the expand output.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* output_c
        if self._index is NULL:
            errorinfo = campl.AMPL_EntityExpand(self._ampl._c_ampl, self._name, &output_c)
        else:
            errorinfo = campl.AMPL_InstanceExpand(self._ampl._c_ampl, self._name, self._index, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)
        return output

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        assert self.wrap_function is not None
        return InstanceIterator.create(self._ampl, self._name, self.wrap_function, self)

    def __getitem__(self, index):
        if not isinstance(index, (tuple, list)):
            index = [index]
        if len(index) == 0:
            self._check_empty_index()
        cdef campl.AMPL_TUPLE* tuple_c =  to_c_tuple(index)
        return create_entity(self.wrap_function, self._ampl, self._name, tuple_c, self)

    def get(self, *index):
        """
        Get the instance with the specified index. For a parameter, the value
        of that instance is returned instead (as with ``p[index]``).

        If no index is passed, this object itself is returned. For an indexed
        entity it then still represents the whole family, so instance-level
        accessors such as ``get().value()`` raise :class:`TypeError`.

        Returns:
            The corresponding instance.
        """
        assert self.wrap_function is not None
        cdef campl.AMPL_TUPLE* tuple_c
        if len(index) == 1 and isinstance(index[0], (tuple, list)):
            index = index[0]
            index = list(index)
        if len(index) == 0:
            return self
        tuple_c = to_c_tuple(index)
        if self.wrap_function == campl.AMPL_PARAMETER:
            try:
                return _get_parameter_value(self._ampl, self._name, tuple_c)
            finally:
                campl.AMPL_TupleFree(&tuple_c)
        return create_entity(self.wrap_function, self._ampl, self._name, tuple_c, self)

    def find(self, index):
        """
        Searches the current entity for an instance with the specified index.
        The only instance of a scalar entity has the empty index ``()``.

        Returns:
            The wanted instance if found, otherwise it returns `None`.
        """
        assert self.wrap_function is not None
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef size_t i
        cdef campl.AMPL_TUPLE* index_c
        cdef campl.AMPL_TUPLE** indices_c
        cdef size_t size
        cdef campl.AMPL_ENTITYTYPE entitytype
        if not isinstance(index, (tuple, list)):
            index = [index]
        if self._family_indexarity() == 0:
            # AMPL also reports indexarity 0 for a deleted entity: make sure
            # the entity exists, so that this raises KeyError as for an
            # indexed entity instead of reporting a missing instance.
            PY_AMPL_CALL(campl.AMPL_EntityGetType(self._ampl._c_ampl, self._name, &entitytype))
            # A scalar entity has no tuples to search (AMPL_EntityGetTuples
            # must not be called for it): an empty index names the entity
            # itself, as with x[()], and any other index has no instance.
            if len(index) != 0:
                return None
            index_c = to_c_tuple(index)
            return create_entity(self.wrap_function, self._ampl, self._name, index_c, self)
        index_c = to_c_tuple(index)
        errorinfo = campl.AMPL_EntityGetTuples(self._ampl._c_ampl, self._name, &indices_c, &size)
        if errorinfo:
            campl.AMPL_TupleFree(&index_c)
            PY_AMPL_CALL(errorinfo)
        for i in range(size):
            if campl.AMPL_TupleCompare(index_c, indices_c[i]) == 0:
                for j in range(size):
                    campl.AMPL_TupleFree(&indices_c[j])
                free(indices_c)
                return create_entity(self.wrap_function, self._ampl, self._name, index_c, self)
        for i in range(size):
            campl.AMPL_TupleFree(&indices_c[i])
        free(indices_c)
        campl.AMPL_TupleFree(&index_c)
        return None

    def instances(self):
        """
        Get all the instances in this entity.
        """
        return InstanceIterator.create(self._ampl, self._name, self.wrap_function, self)

    def name(self):
        """
        Get the name of this entity.
        """
        return self._name.decode('utf-8')

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
        if self._is_instance():
            return 0
        return self._family_indexarity()

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
        PY_AMPL_CALL(campl.AMPL_EntityGetNumInstances(self._ampl._c_ampl, self._name, &size))
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
        PY_AMPL_CALL(campl.AMPL_EntityGetIndexingSets(self._ampl._c_ampl, self._name, &sets, &size))
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
        PY_AMPL_CALL(campl.AMPL_EntityGetXref(self._ampl._c_ampl, self._name, &xref, &size))
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
            PY_AMPL_CALL(campl.AMPL_EntityGetValues(self._ampl._c_ampl, self._name, NULL, n, &df_c))
        else:
            if isinstance(suffixes, str):
                suffixes = [suffixes]
            else:
                suffixes = list(map(str, suffixes))
            suffixes_c = <char**> malloc(len(suffixes) * sizeof(char*))
            for i in range(len(suffixes)):
                suffixes_c[i] = strdup(suffixes[i].encode('utf-8'))
            n = len(suffixes)
            PY_AMPL_CALL(campl.AMPL_EntityGetValues(self._ampl._c_ampl, self._name, <const char* const*>suffixes_c, n, &df_c))
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

        Raises:
            ValueError: if the number of index columns of the data does not
            match the indexarity of the entity.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef DataFrame df = None
        cdef size_t indexarity
        cdef char* _name_c = NULL
        if isinstance(data, DataFrame):
            df = data
            indexarity = self.indexarity()
        elif isinstance(data, dict):
            if not data:
                # Nothing to assign, and an empty dict states no index arity.
                return
            df = DataFrame.from_dict(data)
            indexarity = self.indexarity()
        elif pd is not None and isinstance(data, (pd.DataFrame, pd.Series)):
            indexarity = self.indexarity()
            df = DataFrame.from_pandas(data, indexarity=indexarity)
        else:
            raise TypeError(f"Unexpected data type: {type(data)}.")
        PY_AMPL_CALL(campl.AMPL_InstanceGetName(self._ampl._c_ampl, self._name, self._index, &_name_c))
        try:
            if not self._has_rows_to_assign(df, indexarity, _name_c.decode('utf-8')):
                return
            errorinfo = campl.AMPL_EntitySetValues(self._ampl._c_ampl, _name_c, df.get_ptr())
            if errorinfo:
                PY_AMPL_CALL(errorinfo)
        finally:
            campl.AMPL_StringFree(&_name_c)

    # Aliases
    toString = to_string
    getIndexingSets = get_indexing_sets
    getValues = get_values
    isScalar = is_scalar
    numInstances = num_instances
    setValues = set_values
