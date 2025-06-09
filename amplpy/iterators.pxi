cdef class EnvIterator(object):
    cdef campl.AMPL_ENVIRONMENT* env_c
    cdef campl.AMPL_ENVIRONMENTVAR* begin
    cdef campl.AMPL_ENVIRONMENTVAR* end
    cdef campl.AMPL_ENVIRONMENTVAR* iterator

    @staticmethod
    cdef create(campl.AMPL_ENVIRONMENT* env_c):
        envit = EnvIterator()
        envit.env_c = env_c
        envit.begin = NULL
        envit.end = NULL
        envit.iterator = NULL
        campl.AMPL_EnvironmentGetEnvironmentVar(envit.env_c, &envit.begin)
        cdef size_t size
        campl.AMPL_EnvironmentGetSize(envit.env_c, &size)
        envit.end = envit.begin + size
        envit.iterator = envit.begin
        return envit

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self.end:
            raise StopIteration
        cdef campl.AMPL_ENVIRONMENTVAR* it = self.iterator
        self.iterator += 1
        cdef char* name_c
        cdef char* value_c
        campl.AMPL_EnvironmentVarGetName(it, &name_c)
        campl.AMPL_EnvironmentVarGetValue(it, &value_c)
        name = name_c.decode('utf-8', errors='replace')
        value = value_c.decode('utf-8', errors='replace')
    
        return (name, value)

cdef class EntityMap(object):
    cdef AMPL _ampl
    cdef campl.AMPL_ENTITYTYPE entity_class
    cdef char** begin
    cdef size_t iterator
    cdef size_t _size

    @staticmethod
    cdef create(AMPL ampl, campl.AMPL_ENTITYTYPE entity_class):
        cdef campl.AMPL_ERRORINFO* errorinfo
        entityit = EntityMap()
        entityit._ampl = ampl
        entityit.entity_class = entity_class
        if entity_class == campl.AMPL_VARIABLE:
            errorinfo = campl.AMPL_GetVariables(entityit._ampl._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_CONSTRAINT:
            errorinfo = campl.AMPL_GetConstraints(entityit._ampl._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_OBJECTIVE:
            errorinfo = campl.AMPL_GetObjectives(entityit._ampl._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_SET:
            errorinfo = campl.AMPL_GetSets(entityit._ampl._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_PARAMETER:
            errorinfo = campl.AMPL_GetParameters(entityit._ampl._c_ampl, &entityit._size, &entityit.begin)
        else:
            raise ValueError(f"Unknown entity class.")

        if errorinfo:
            for i in range(entityit._size):
                campl.AMPL_StringFree(&entityit.begin[i])
            free(entityit.begin)
            PY_AMPL_CALL(errorinfo)

        entityit.iterator = 0
        return entityit

    def __dealloc__(self):
        if self.iterator < self._size:
            for i in range(self.iterator, self._size):
                campl.AMPL_StringFree(&self.begin[i])
        if self.begin != NULL:
            free(self.begin)
            self.begin = NULL

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self._size:
            raise StopIteration
        tuple = (self.begin[self.iterator].decode('utf-8'), create_entity(self.entity_class, self._ampl, self.begin[self.iterator], NULL, None))
        self.iterator += 1
        return tuple

    def __getitem__(self, key):
        assert isinstance(key, str)
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(key.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._ampl._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != self.entity_class:
            free(name_c)
            raiseKeyError(self.entity_class, key)
        return create_entity(self.entity_class, self._ampl, name_c, NULL, None)

    def size(self):
        return int(self._size)

    def __len__(self):
        return self.size()

cdef class InstanceIterator(object):
    cdef AMPL _ampl
    cdef char* _name
    cdef campl.AMPL_ENTITYTYPE entity_class
    cdef campl.AMPL_TUPLE** begin
    cdef size_t iterator
    cdef size_t _size
    cdef object _entity

    @staticmethod
    cdef create(AMPL ampl, char* name, campl.AMPL_ENTITYTYPE entity_class, parent):
        cdef campl.AMPL_ERRORINFO* errorinfo
        instanceit = InstanceIterator()
        cdef size_t arity
        instanceit._ampl = ampl
        instanceit._name = name
        instanceit.entity_class = entity_class
        instanceit._entity = parent
        PY_AMPL_CALL(campl.AMPL_EntityGetIndexarity(instanceit._ampl._c_ampl, instanceit._name, &arity))
        if arity == 0:
            instanceit._size = 1
            instanceit.begin = NULL
            instanceit.iterator = 0
            return instanceit
        errorinfo = campl.AMPL_EntityGetTuples(instanceit._ampl._c_ampl, instanceit._name, &instanceit.begin, &instanceit._size)
        if errorinfo:
            for i in range(instanceit._size):
                campl.AMPL_TupleFree(&instanceit.begin[i])
            free(instanceit.begin)
            PY_AMPL_CALL(errorinfo)
        if instanceit._size == 0:
            instanceit.iterator = 0
        else:
            instanceit.iterator = 0
        return instanceit

    def __dealloc__(self):
        if self.iterator+1 < self._size:
            for i in range(self.iterator+1, self._size):
                campl.AMPL_TupleFree(&self.begin[i])
        if self.begin != NULL:
            free(self.begin)
            self.begin = NULL

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self._size:
            raise StopIteration
        self.iterator += 1
        if self.begin == NULL:
            return (None, self._entity)
        else:
            return (to_py_tuple(self.begin[self.iterator-1]), create_entity(self.entity_class, self._ampl, self._name, self.begin[self.iterator-1], self._entity))

    def __getitem__(self, key):
        assert isinstance(key, str)
        key = tuple(key)
        cdef campl.AMPL_TUPLE* tuple_c = to_c_tuple(key)
        return create_entity(self.entity_class, self._ampl, self._name, tuple_c, self._entity)

    def size(self):
        return int(self._size)

    def __len__(self):
        return self.size()


cdef class MemberRangeIterator(object):
    """Iterator for set members."""
    cdef campl.AMPL* _c_ampl
    cdef char* _name
    cdef campl.AMPL_TUPLE* _index
    cdef campl.AMPL_TUPLE** begin
    cdef size_t iterator
    cdef size_t _size
    cdef object _entity

    @staticmethod
    cdef create(campl.AMPL* ampl, char* name, campl.AMPL_TUPLE* index, parent):
        cdef campl.AMPL_ERRORINFO* errorinfo
        instanceit = MemberRangeIterator()
        instanceit._c_ampl = ampl
        instanceit._name = name
        instanceit._index = index
        instanceit._entity = parent
        if instanceit._entity is not None:
            Py_INCREF(instanceit._entity)
        errorinfo = campl.AMPL_SetInstanceGetValues(instanceit._c_ampl, instanceit._name, instanceit._index, &instanceit.begin, &instanceit._size)
        if errorinfo:
            for i in range(instanceit._size):
                campl.AMPL_TupleFree(&instanceit.begin[i])
            free(instanceit.begin)
            PY_AMPL_CALL(errorinfo)
        instanceit.iterator = 0
        return instanceit

    def __dealloc__(self):
        if self._entity is not None:
            Py_DECREF(self._entity)
        for i in range(self._size):
            campl.AMPL_TupleFree(&self.begin[i])
        if self.begin != NULL:
            free(self.begin)
            self.begin = NULL

    def size(self):
        return int(self._size)

    def __len__(self):
        return self.size()

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self._size:
            raise StopIteration
        cdef campl.AMPL_TUPLE* it = self.begin[self.iterator]
        cdef size_t size
        cdef campl.AMPL_VARIANT* variant
        campl.AMPL_TupleGetSize(it, &size)
        if size == 1:
            campl.AMPL_TupleGetVariant(it, 0, &variant)
            py_variant = to_py_variant(variant)
            self.iterator += 1
            return py_variant
        else:
            py_tuple = to_py_tuple(it)
            self.iterator += 1
            return py_tuple

cdef class ColIterator(object):
    cdef campl.AMPL_DATAFRAME* _df
    cdef size_t _index
    cdef size_t _rowsize
    cdef size_t _rowit

    @staticmethod
    cdef create(campl.AMPL_DATAFRAME* df, size_t index):
        colit = ColIterator()
        colit._df = df
        colit._index = index
        colit._rowit = 0
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumRows(colit._df, &colit._rowsize))
        return colit

    def __iter__(self):
        return self

    def __next__(self):
        cdef campl.AMPL_VARIANT* v
        if self._rowit >= self._rowsize:
            raise StopIteration
        PY_AMPL_CALL(campl.AMPL_DataFrameElement(self._df, self._rowit, self._index, &v))
        self._rowit += 1
        return to_py_variant(v)

cdef class RowIterator(object):
    cdef campl.AMPL_DATAFRAME* _df
    cdef size_t _index
    cdef size_t _columnsize
    cdef size_t _columnit

    @staticmethod
    cdef create(campl.AMPL_DATAFRAME* df, size_t index):
        rowit = RowIterator()
        rowit._df = df
        rowit._index = index
        rowit._columnit = 0
        PY_AMPL_CALL(campl.AMPL_DataFrameGetNumCols(rowit._df, &rowit._columnsize))
        return rowit

    def __iter__(self):
        return self

    def __next__(self):
        cdef campl.AMPL_VARIANT* v
        if self._columnit >= self._columnsize:
            raise StopIteration
        PY_AMPL_CALL(campl.AMPL_DataFrameElement(self._df, self._index, self._columnit, &v))
        self._columnit += 1
        return to_py_variant(v)
