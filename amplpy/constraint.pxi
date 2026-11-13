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
        Drop this constraint instance, or all instances if called on the
        constraint entity.
        """
        if self._index is NULL:
            PY_AMPL_CALL(campl.AMPL_EntityDrop(self._ampl._c_ampl, self._name))
        else:
            PY_AMPL_CALL(campl.AMPL_InstanceDrop(self._ampl._c_ampl, self._name, self._index))

    def restore(self):
        """
        Restore this constraint instance, or all instances if called on the
        constraint entity.
        """
        if self._index is NULL:
            PY_AMPL_CALL(campl.AMPL_EntityRestore(self._ampl._c_ampl, self._name))
        else:
            PY_AMPL_CALL(campl.AMPL_InstanceRestore(self._ampl._c_ampl, self._name, self._index))

    def body(self):
        """
        Get the current value of the constraint's body.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_BODY)

    def astatus(self):
        """
        Get the current AMPL status (dropped, presolved, or substituted out).
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_ASTATUS)

    def defvar(self):
        """
        Get the index in `_var` of "defined variable" substituted out by the
        constraint.
        """
        return self._get_int_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_DEFVAR)

    def dinit(self):
        """
        Get the current initial guess for the constraint's dual variable.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_DINIT)

    def dinit0(self):
        """
        Get the original initial guess for the constraint's dual variable.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_DINIT0)

    def dual(self):
        """
        Get the current value of the constraint's dual variable.

        Note that dual values are often reset by the underlying AMPL
        interpreter by the presolve functionalities triggered by some methods.
        A possible workaround is to set the option `presolve` to `false`
        (see :func:`~amplpy.AMPL.setOption`).
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_DUAL)

    def lb(self):
        """
        Get the current value of the constraint's lower bound.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_LB)

    def ub(self):
        """
        Get the current value of the constraint's upper bound.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_UB)

    def lbs(self):
        """
        Get the constraint lower bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_LBS)

    def ubs(self):
        """
        Get the constraint upper bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_UBS)

    def ldual(self):
        """
        Get the current dual value associated with the lower bound.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_LDUAL)

    def udual(self):
        """
        Get the current dual value associated with the upper bounds.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_UDUAL)

    def lslack(self):
        """
        Get the slack at lower bound `body - lb`.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_LSLACK)

    def uslack(self):
        """
        Get the slack at upper bound `ub - body`.
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_USLACK)

    def slack(self):
        """
        Constraint slack (the lesser of lslack and uslack).
        """
        return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_SLACK)

    def sstatus(self):
        """
        Get the solver status (basis status of constraint's slack or artificial
        variable).
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_SSTATUS)

    def status(self):
        """
        Get the AMPL status if not `in`, otherwise solver status.
        """
        return self._get_string_suffix(campl.AMPL_STRINGSUFFIX.AMPL_STATUS)

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

        Raises:
            TypeError: if this is an indexed constraint.
        """
        self._check_scalar()
        PY_AMPL_CALL(campl.AMPL_ConstraintInstanceSetDual(self._ampl._c_ampl, self._name, self._index, float(dual)))

    def val(self):
        """
        Get the AMPL val suffix. Valid only for logical constraints.
        """
        if self.is_logical():
            return self._get_double_suffix(campl.AMPL_NUMERICSUFFIX.AMPL_VAL)
        else:
            return None

    # Aliases
    isLogical = is_logical
    setDual = set_dual
