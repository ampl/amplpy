# -*- coding: utf-8 -*-
from libcpp cimport bool as bool_c



cdef class Constraint(Entity):
    """
    Bases: :class:`~amplpy.Entity`.

    This class represents an algebraic or logical constraint. In case the
    constraint is scalar, its values can be accessed via functions like
    :func:`~amplpy.Constraint.body` and :func:`~amplpy.Constraint.dual`.
    All the AMPL suffixes for constraints (see
    http://www.ampl.com/NEW/suffbuiltin.html)
    are available through methods of this class with the same name (and methods
    of ConstraintInstance for indexed constraints).

    Note that, since this class represents both algebraic and logical
    constraints, some suffixes might not be available for every entity.

    An TypeError is thrown if one of such methods is called for
    a non-scalar constraint and if a method corresponding to a suffix which is
    not supported by the type of the constraint is called.
    A runtime error is thrown if any property of an entity which has been
    deleted from the underlying interpreter is accessed.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), see
    :func:`~amplpy.Entity.get_values`
    and the :class:`~amplpy.DataFrame` class.
    """
    @staticmethod
    cdef create(AMPL ampl, char* name, campl.AMPL_TUPLE* index, parent):
        entity = Constraint()
        entity._ampl = ampl
        Py_INCREF(entity._ampl)
        entity._name = name
        entity._index = index
        entity.wrap_function = campl.AMPL_CONSTRAINT
        entity._entity = parent
        if entity._entity is not None:
            Py_INCREF(entity._entity)
        return entity

    def __setitem__(self, index, value):
        self.__getitem__(index).set_dual(value)

    def is_logical(self):
        """
        Check if the constraint is a logical constraint. Returns True if
        logical. The available suffixes differ between logical and non logical
        constraints. See http://www.ampl.com/NEW/suffbuiltin.html for a list of
        the available suffixes for algebraic constraints. The suffixes
        available for logical constraints are marked on the method description
        by "Valid only for logical constraints".
        """
        cdef bool_c value
        try:
            PY_AMPL_CALL(campl.AMPL_ConstraintIsLogical(self._ampl._c_ampl, self._name, &value))
            return value
        except AttributeError:
            return False

    def drop(self):
        """
        Drop all instances in this constraint entity, corresponding to the AMPL
        code: `drop constraintname;`.
        """
        PY_AMPL_CALL(campl.AMPL_EntityDrop(self._ampl._c_ampl, self._name))

    def restore(self):
        """
        Restore all instances in this constraint entity, corresponding to the
        AMPL code: `restore constraintname;`.
        """
        PY_AMPL_CALL(campl.AMPL_EntityRestore(self._ampl._c_ampl, self._name))

    def body(self):
        """
        Get the current value of the constraint's body.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_BODY, &value))
        return value

    def astatus(self):
        """
        Get the current AMPL status (dropped, presolved, or substituted out).
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_ASTATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def defvar(self):
        """
        Get the index in `_var` of "defined variable" substituted out by the
        constraint.
        """
        cdef int value
        PY_AMPL_CALL(campl.AMPL_InstanceGetIntSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DEFVAR, &value))
        return value

    def dinit(self):
        """
        Get the current initial guess for the constraint's dual variable.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DINIT, &value))
        return value

    def dinit0(self):
        """
        Get the original initial guess for the constraint's dual variable.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DINIT0, &value))
        return value

    def dual(self):
        """
        Get the current value of the constraint's dual variable.

        Note that dual values are often reset by the underlying AMPL
        interpreter by the presolve functionalities triggered by some methods.
        A possible workaround is to set the option `presolve` to `false`
        (see :func:`~amplpy.AMPL.setOption`).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_DUAL, &value))
        return value

    def lb(self):
        """
        Get the current value of the constraint's lower bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LB, &value))
        return value

    def ub(self):
        """
        Get the current value of the constraint's upper bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UB, &value))
        return value

    def lbs(self):
        """
        Get the constraint lower bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LBS, &value))
        return value

    def ubs(self):
        """
        Get the constraint upper bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UBS, &value))
        return value

    def ldual(self):
        """
        Get the current dual value associated with the lower bound.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LDUAL, &value))
        return value

    def udual(self):
        """
        Get the current dual value associated with the upper bounds.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_UDUAL, &value))
        return value

    def lslack(self):
        """
        Get the slack at lower bound `body - lb`.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_LSLACK, &value))
        return value

    def uslack(self):
        """
        Get the slack at upper bound `ub - body`.
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_USLACK, &value))
        return value

    def slack(self):
        """
        Constraint slack (the lesser of lslack and uslack).
        """
        cdef double value
        PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_SLACK, &value))
        return value

    def sstatus(self):
        """
        Get the solver status (basis status of constraint's slack or artificial
        variable).
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
        Get the AMPL status if not `in`, otherwise solver status.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* value_c
        errorinfo = campl.AMPL_InstanceGetStringSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_STRINGSUFFIX.AMPL_STATUS, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        value = str(value_c.decode('utf-8'))
        campl.AMPL_StringFree(&value_c)

        return value

    def set_dual(self, dual):
        """
        Set the value of the dual variable associated to this constraint (valid
        only if the constraint is scalar). Equivalent to the AMPL statement:

        `let c := dual;`

        Note that dual values are often reset by the underlying AMPL
        interpreter by the presolve functionalities triggered by some methods.
        A possible workaround is to set the option `presolve` to `False`
        (see :func:`~amplpy.AMPL.setOption`).

        Args:
            dual: The value to be assigned to the dual variable.
        """
        PY_AMPL_CALL(campl.AMPL_ConstraintInstanceSetDual(self._ampl._c_ampl, self._name, self._index, float(dual)))

    def val(self):
        """
        Get the AMPL val suffix. Valid only for logical constraints.
        """
        cdef double value
        if self.is_logical():
            PY_AMPL_CALL(campl.AMPL_InstanceGetDoubleSuffix(self._ampl._c_ampl, self._name, self._index, campl.AMPL_NUMERICSUFFIX.AMPL_VAL, &value))
            return value
        else:
            return None

    # Aliases
    isLogical = is_logical
    setDual = set_dual
