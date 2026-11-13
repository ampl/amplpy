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
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_VALUE)

    def astatus(self):
        """
        Return the AMPL status.
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_ASTATUS)

    def sstatus(self):
        """
        Return the solver status.
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_SSTATUS)

    def exitcode(self):
        """
        Exit code returned by solver after most recent solve with this
        objective.
        """
        return self._get_int_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_EXITCODE)

    def message(self):
        """
        Result message returned by solver after most recent solve with this
        objective.
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_MESSAGE)

    def result(self):
        """
        Result string returned by solver after most recent solve with this
        objective.
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_RESULT)

    def drop(self):
        """
        Drop this objective instance, or all instances if called on the
        objective entity.
        """
        if self._index is NULL:
            PY_AMPL_CALL(campl.AMPL_EntityDrop(self._ampl._c_ampl, self._name))
        else:
            PY_AMPL_CALL(campl.AMPL_InstanceDrop(self._ampl._c_ampl, self._name, self._index))

    def restore(self):
        """
        Restore this objective instance, or all instances if called on the
        objective entity (no effect if already restored).
        """
        if self._index is NULL:
            PY_AMPL_CALL(campl.AMPL_EntityRestore(self._ampl._c_ampl, self._name))
        else:
            PY_AMPL_CALL(campl.AMPL_InstanceRestore(self._ampl._c_ampl, self._name, self._index))

    def minimization(self):
        """
        Get the sense of this objective. Returns True if minimize,
        False if maximize.
        """
        value = self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_SENSE)
        if value == 'minimize':
            return True
        else:
            return False
