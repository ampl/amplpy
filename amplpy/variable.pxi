# -*- coding: utf-8 -*-

cdef class Variable(Entity):
    """
    Bases: :class:`~amplpy.Entity`.

    Represents an AMPL decision variable. Note that, in case of a scalar
    variable, all the properties of the variable instance can be accessed
    through methods like :func:`~amplpy.Variable.value`. The methods have the
    same name of the corresponding AMPL suffixes.
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
    cdef create(AMPL ampl, char *name, campl.AMPL_TUPLE* index, parent):
        entity = Variable()
        entity._ampl = ampl
        Py_INCREF(entity._ampl)
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_VARIABLE
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def __setitem__(self, index, value):
        self.__getitem__(index).set_value(value)

    def value(self):
        """
        Get the current value of this variable.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_VALUE, &value))
        return value

    def fix(self, value=None):
        """
        Fix all instances of this variable to a value if provided or to
        their current value otherwise.

        Args:
            value: value to be set.
        """
        if value is None:
            PY_AMPL_CALL(campl.AMPL_VariableInstanceFix(self._ampl._c_ampl, self._name, self._index))
        else:
            PY_AMPL_CALL(campl.AMPL_VariableInstanceFixToValue(self._ampl._c_ampl, self._name, self._index, value))

    def unfix(self):
        """
        Unfix all instances of this variable.
        """
        PY_AMPL_CALL(campl.AMPL_VariableInstanceUnfix(self._ampl._c_ampl, self._name, self._index))

    def set_value(self, value):
        """
        Set the current value of this variable (does not fix it),
        equivalent to the AMPL command `let`.

        Args:
            value: value to be set.
        """
        if isinstance(value, Parameter):
            PY_AMPL_CALL(campl.AMPL_VariableInstanceSetValue(self._ampl._c_ampl, self._name, self._index, value.value()))
        else:
            PY_AMPL_CALL(campl.AMPL_VariableInstanceSetValue(self._ampl._c_ampl, self._name, self._index, float(value)))

    def astatus(self):
        """
        Get the AMPL status (fixed, presolved, or substituted out).
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_ASTATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def defeqn(self):
        """
        Get the index in `_con` of "defining constraint" used to substitute
        variable out.
        """
        cdef int value
        PY_AMPL_CALL(campl.AMPL_InstanceGetIntSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DEFEQN, &value))
        return value

    def dual(self):
        """
        Get the dual value on defining constraint of variable substituted out.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DUAL, &value))
        return value

    def init(self):
        """
        Get the current initial guess.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_INIT, &value))
        return value

    def init0(self):
        """
        Get the original initial guess (set by `:=` or`default` or by a data
        statement).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_INIT0, &value))
        return value

    def lb(self):
        """
        Returns the current lower bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LB, &value))
        return value

    def ub(self):
        """
        Returns the current upper bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UB, &value))
        return value

    def lb0(self):
        """
        Returns the initial lower bounds, from the var declaration.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LB0, &value))
        return value

    def ub0(self):
        """
        Returns the initial upper bound, from the var declaration.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UB0, &value))
        return value

    def lb1(self):
        """
        Returns the weaker lower bound from AMPL's presolve phase.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LB1, &value))
        return value

    def ub1(self):
        """
        Returns the weaker upper bound from AMPL's presolve phase.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UB1, &value))
        return value

    def lb2(self):
        """
        Returns the stronger lower bound from AMPL's presolve phase.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LB2, &value))
        return value

    def ub2(self):
        """
        Returns the stronger upper bound from AMPL's presolve phase.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UB2, &value))
        return value

    def lrc(self):
        """
        Returns the reduced cost at lower bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LRC, &value))
        return value

    def urc(self):
        """
        Returns the reduced cost at upper bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_URC, &value))
        return value

    def lslack(self):
        """
        Return the slack at lower bound (``val - lb``).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LSLACK, &value))
        return value

    def uslack(self):
        """
        Return the slack at upper bound (``ub - val``).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_USLACK, &value))
        return value

    def rc(self):
        """
        Get the reduced cost (at the nearer bound).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_RC, &value))
        return value

    def slack(self):
        """
        Returns the bound slack which is the lesser of
        :func:`~amplpy.Variable.lslack` and :func:`~amplpy.Variable.uslack`.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_SLACK, &value))
        return value

    def sstatus(self):
        """
        Solver status (basis status of variable).
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_SSTATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def status(self):
        """
        AMPL status if not `in`, otherwise solver status.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_STATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    # Aliases
    setValue = set_value
