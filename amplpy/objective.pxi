# -*- coding: utf-8 -*-


cdef class Objective(Entity):
    """
    Bases: :class:`~amplpy.Entity`.

    Represents an AMPL objective. Note that, in case of a scalar objective, all
    the properties (corresponding to AMPL suffixes) of the objective instance
    can be accessed through methods like :func:`~amplpy.Objective.value`.
    The methods have the same name of the corresponding AMPL suffixes.
    See http://www.ampl.com/NEW/suffbuiltin.html for a list of the available
    suffixes.

    All these methods throw a TypeError if called for a non scalar
    objective and an RuntimeError if called on an entity which has been deleted
    in the underlying intepreter.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), see
    :func:`~amplpy.Entity.get_values`
    and the :class:`~amplpy.DataFrame` class.
    """
    @staticmethod
    cdef create(AMPL ampl, char* name, campl.AMPL_TUPLE* index, parent):
        entity = Objective()
        entity._ampl = ampl
        Py_INCREF(entity._ampl)
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_OBJECTIVE
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def value(self):
        """
        Get the value of the objective.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_VALUE, &value))
        return value

    def astatus(self):
        """
        Return the AMPL status.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_ASTATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def sstatus(self):
        """
        Return the solver status.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_SSTATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def exitcode(self):
        """
        Exit code returned by solver after most recent solve with this
        objective.
        """
        cdef int value
        PY_AMPL_CALL(campl.AMPL_InstanceGetIntSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_EXITCODE, &value))
        return value

    def message(self):
        """
        Result message returned by solver after most recent solve with this
        objective.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_MESSAGE, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def result(self):
        """
        Result string returned by solver after most recent solve with this
        objective.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_RESULT, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def drop(self):
        """
        Drop this objective instance.
        """
        PY_AMPL_CALL(campl.AMPL_EntityDrop(self._ampl._c_ampl, self._name))

    def restore(self):
        """
        Restore this objective (if it had been dropped, no effect otherwise).
        """
        PY_AMPL_CALL(campl.AMPL_EntityRestore(self._ampl._c_ampl, self._name))

    def minimization(self):
        """
        Get the sense of this objective. Returns True if minimize,
        False if maximize.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_SENSE, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        if value == 'minimize':
            return True
        else:
            return False
