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
        name = name_c.decode('utf-8')
        value = value_c.decode('utf-8')
        return (name, value)


cdef class EntityMap(object):
    cdef campl.AMPL* _c_ampl
    cdef campl.AMPL_ENTITYTYPE entity_class
    cdef char** begin
    cdef char** end
    cdef char** iterator
    cdef size_t _size

    @staticmethod
    cdef create(campl.AMPL* ampl, campl.AMPL_ENTITYTYPE entity_class):
        entityit = EntityMap()
        entityit._c_ampl = ampl
        entityit.entity_class = entity_class
        if entity_class == campl.AMPL_VARIABLE:
            campl.AMPL_GetVariables(entityit._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_CONSTRAINT:
            campl.AMPL_GetConstraints(entityit._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_OBJECTIVE:
            campl.AMPL_GetObjectives(entityit._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_SET:
            campl.AMPL_GetSets(entityit._c_ampl, &entityit._size, &entityit.begin)
        elif entity_class == campl.AMPL_PARAMETER:
            campl.AMPL_GetParameters(entityit._c_ampl, &entityit._size, &entityit.begin)
        else:
            raise ValueError(f"Unknown entity class.")

        entityit.iterator = entityit.begin
        entityit.end = entityit.begin + entityit._size
        return entityit

    def __iter__(self):
        self.iterator = self.begin
        return self

    def __next__(self):
        if self.iterator >= self.end:
            raise StopIteration
        cdef char** it = self.iterator
        self.iterator += 1
        name = it[0].decode('utf-8')
        return (name, m(self.entity_class, self._c_ampl, name, NULL))

    def __getitem__(self, key):
        assert isinstance(key, str)
        cdef campl.AMPL_ENTITYTYPE entitytype
        PY_AMPL_CALL(campl.AMPL_EntityGetType(self._c_ampl, key.encode('utf-8'), &entitytype))
        if entitytype != self.entity_class: raiseKeyError(self.entity_class, key)
        return m(self.entity_class, self._c_ampl, key, NULL)

    def size(self):
        return int(self._size)

    def __len__(self):
        return self.size()

cdef class InstanceIterator(object):
    
    cdef campl.AMPL* _c_ampl
    cdef str _name
    cdef campl.AMPL_ENTITYTYPE entity_class
    cdef campl.AMPL_TUPLE** begin
    cdef campl.AMPL_TUPLE** end
    cdef size_t iterator
    cdef size_t _size

    @staticmethod
    cdef create(campl.AMPL* ampl, name, campl.AMPL_ENTITYTYPE entity_class):
        instanceit = InstanceIterator()
        cdef size_t arity
        instanceit._c_ampl = ampl
        instanceit._name = name
        instanceit.entity_class = entity_class
        campl.AMPL_EntityGetIndexarity(instanceit._c_ampl, instanceit._name.encode('utf-8'), &arity)
        if arity == 0:
            instanceit._size = 1
            instanceit.begin = NULL
            instanceit.iterator = 0
            instanceit.end = NULL
            return instanceit
        campl.AMPL_EntityGetTuples(instanceit._c_ampl, instanceit._name.encode('utf-8'), &instanceit.begin, &instanceit._size)
        if instanceit._size == 0:
            instanceit.iterator = 0
            instanceit.end = NULL
        else:
            instanceit.iterator = -1
            instanceit.end = instanceit.begin + instanceit._size
        return instanceit

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self._size:
            raise StopIteration
        self.iterator += 1
        if self.begin == NULL:
            return (None, m(self.entity_class, self._c_ampl, self._name, NULL))
        else:
            return (to_py_tuple(self.begin[self.iterator]), m(self.entity_class, self._c_ampl, self._name, self.begin[self.iterator]))

    def __getitem__(self, key):
        assert isinstance(key, str)
        key = tuple(key)
        cdef campl.AMPL_TUPLE* tuple_c = to_c_tuple(key)
        return m(self.entity_class, self._c_ampl, self._name, tuple_c)

    def size(self):
        return int(self._size)

    def __len__(self):
        return self.size()


cdef class MemberRangeIterator(object):
    """Iterator for set members."""
    cdef campl.AMPL* _c_ampl
    cdef str _name
    cdef campl.AMPL_TUPLE* _index
    cdef campl.AMPL_TUPLE** begin
    cdef campl.AMPL_TUPLE** end
    cdef campl.AMPL_TUPLE** iterator
    cdef size_t _size

    @staticmethod
    cdef create(campl.AMPL* ampl, name, campl.AMPL_TUPLE* index):
        instanceit = MemberRangeIterator()
        instanceit._c_ampl = ampl
        instanceit._name = name
        instanceit._index = index
        campl.AMPL_SetInstanceGetValues(instanceit._c_ampl, instanceit._name.encode('utf-8'), instanceit._index, &instanceit.begin, &instanceit._size)
        if instanceit._size == 0:
            instanceit.iterator = NULL
            instanceit.end = NULL
        else:
            instanceit.iterator = instanceit.begin
            instanceit.end = instanceit.begin + instanceit._size
        return instanceit

    def size(self):
        cdef size_t size
        campl.AMPL_SetInstanceGetSize(self._c_ampl, self._name.encode('utf-8'), self._index, &size)
        return int(size)

    def __len__(self):
        return self.size()

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator >= self.end or self.iterator == NULL:
            raise StopIteration
        cdef campl.AMPL_TUPLE** it = self.iterator
        cdef size_t size
        cdef campl.AMPL_VARIANT* variant
        campl.AMPL_TupleGetSize(it[0], &size)
        self.iterator += 1
        if size == 1:
            campl.AMPL_TupleGetVariant(it[0], 0, &variant)
            return to_py_variant(variant)
        else:
            return to_py_tuple(it[0])



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
        campl.AMPL_DataFrameGetNumRows(colit._df, &colit._rowsize)
        return colit

    def __iter__(self):
        return self

    def __next__(self):
        cdef campl.AMPL_VARIANT* v
        if self._rowit >= self._rowsize:
            raise StopIteration
        campl.AMPL_DataFrameElement(self._df, self._rowit, self._index, &v)
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
        campl.AMPL_DataFrameGetNumCols(rowit._df, &rowit._columnsize)
        return rowit

    def __iter__(self):
        return self

    def __next__(self):
        cdef campl.AMPL_VARIANT* v
        if self._columnit >= self._columnsize:
            raise StopIteration
        campl.AMPL_DataFrameElement(self._df, self._index, self._columnit, &v)
        self._columnit += 1
        return to_py_variant(v)