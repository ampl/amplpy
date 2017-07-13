# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from .entity import Entity


class Constraint(Entity):
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
    suffixes for that entities), see :func:`~amplpy.Entity.getValues` and
    the :class:`~amplpy.DataFrame` class.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, Constraint)

    def isLogical(self):
        """
        Check if the constraint is a logical constraint. Returns True if
        logical. The available suffixes differ between logical and non logical
        constraints. See http://www.ampl.com/NEW/suffbuiltin.html for a list of
        the available suffixes for algebraic constraints. The suffixes
        available for logical constraints are marked on the method description
        by "Valid only for logical constraints".
        """
        try:
            return self._impl.isLogical()
        except AttributeError:
            return False

    def drop(self):
        """
        Drop all instances in this constraint entity, corresponding to the AMPL
        code: `drop constraintname;`.
        """
        self._impl.drop()

    def restore(self):
        """
        Restore all instances in this constraint entity, corresponding to the
        AMPL code: `restore constraintname;`.
        """
        self._impl.restore()

    def body(self):
        """
        Get the current value of the constraint's body.
        """
        return self._impl.body()

    def astatus(self):
        """
        Get the current AMPL status (dropped, presolved, or substituted out).
        """
        return self._impl.astatus()

    def defvar(self):
        """
        Get the index in `_var` of "defined variable" substituted out by the
        constraint.
        """
        return self._impl.defvar()

    def dinit(self):
        """
        Get the current initial guess for the constraint's dual variable.
        """
        return self._impl.dinit()

    def dinit0(self):
        """
        Get the original initial guess for the constraint's dual variable.
        """
        return self._impl.dinit0()

    def dual(self):
        """
        Get the current value of the constraint's dual variable.

        Note that dual values are often reset by the underlying AMPL
        interpreter by the presolve functionalities triggered by some methods.
        A possible workaround is to set the option `presolve` to `false`
        (see :func:`~amplpy.AMPL.setOption`).
        """
        return self._impl.dual()

    def lb(self):
        """
        Get the current value of the constraint's lower bound.
        """
        return self._impl.lb()

    def ub(self):
        """
        Get the current value of the constraint's upper bound.
        """
        return self._impl.ub()

    def lbs(self):
        """
        Get the constraint lower bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        return self._impl.lbs()

    def ubs(self):
        """
        Get the constraint upper bound sent to the solver (reflecting
        adjustment for fixed variables).
        """
        return self._impl.ubs()

    def ldual(self):
        """
        Get the current dual value associated with the lower bound.
        """
        return self._impl.ldual()

    def udual(self):
        """
        Get the current dual value associated with the upper bounds.
        """
        return self._impl.udual()

    def lslack(self):
        """
        Get the slack at lower bound `body - lb`.
        """
        return self._impl.lslack()

    def uslack(self):
        """
        Get the slack at upper bound `ub - body`.
        """
        return self._impl.uslack()

    def slack(self):
        """
        Constraint slack (the lesser of lslack and uslack).
        """
        return self._impl.slack()

    def sstatus(self):
        """
        Get the solver status (basis status of constraint's slack or artificial
        variable).
        """
        return self._impl.sstatus()

    def status(self):
        """
        Get the AMPL status if not `in`, otherwise solver status.
        """
        return self._impl.status()

    def setDual(self, dual):
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
        self._impl.setDual(dual)

    def val(self):
        """
        Get the AMPL val suffix. Valid only for logical constraints.
        """
        if self.isLogical():
            return self._impl.val()
        else:
            return None
