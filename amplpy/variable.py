from .entity import Entity


class Variable(Entity):
    """
    Bases: :class:`~amplpy.Entity`.

    Represents an AMPL decision variable. Note that, in case of a scalar
    variable, all the properties of the variable instance can be accessed
    through methods like :func:`~amplpy.Variable.value`. The methods have the
    same name of the corresponding AMPL suffixes.
    See http://www.ampl.com/NEW/suffbuiltin.html for a list of the available
    suffixes.

    All these methods throw a LogicError if called for a non scalar
    objective and an RunTimeError if called on an entity which has been deleted
    in the underlying intepreter.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), see :func:`~amplpy.Entity.getValues` and the
    :class:`~amplpy.DataFrame` class.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, Variable)

    def value(self):
        """
        Get the current value of this variable.
        """
        return self._impl.value()

    def value(self):
        """
        Get the current value of this variable.
        """
        return self._impl.value()

    def fix(self, value=None):
        """
        Fix all instances of this variable to a value if provided or to
        their current value otherwise.

        Args:
            value: value to be set.
        """

        if value is None:
            self._impl.fix()
        else:
            self._impl.fix(value)

    def unfix(self):
        """
        Unfix all instances of this variable.
        """
        self._impl.unfix()

    def setValue(self, value):
        """
        Set the current value of this variable (does not fix it),
        equivalent to the AMPL command `let`.

        Args:
            value: value to be set.
        """
        self._impl.setValue(value)

    def astatus(self):
        """
        Get the AMPL status (fixed, presolved, or substituted out).
        """
        return self._impl.astatus()

    def defeqn(self):
        """
        Get the index in `_con` of "defining constraint" used to substitute
        variable out.
        """
        return self._impl.defeqn()

    def dual(self):
        """
        Get the dual value on defining constraint of variable substituted out.
        """
        return self._impl.dual()

    def init(self):
        """
        Get the current initial guess.
        """
        return self._impl.init()

    def init0(self):
        """
        Get the original initial guess (set by `:=` or`default` or by a data
        statement).
        """
        return self._impl.init0()

    def lb(self):
        """
        Returns the current lower bound. See :ref:`secVariableSuffixesNotes`.
        """
        return self._impl.lb()

    def ub(self):
        """
        Returns the current upper bound. See :ref:`secVariableSuffixesNotes`.
        """
        return self._impl.ub()

    def lb0(self):
        """
        Returns the initial lower bounds, from the var declaration.
        """
        return self._impl.lb0()

    def ub0(self):
        """
        Returns the initial upper bound, from the var declaration.
        """
        return self._impl.ub0()

    def lb1(self):
        """
        Returns the weaker lower bound from AMPL's presolve phase.
        """
        return self._impl.lb1()

    def ub1(self):
        """
        Returns the weaker upper bound from AMPL's presolve phase.
        """
        return self._impl.ub1()

    def lb2(self):
        """
        Returns the stronger lower bound from AMPL's presolve phase.
        """
        return self._impl.lb2()

    def ub2(self):
        """
        Returns the stronger upper bound from AMPL's presolve phase.
        """
        return self._impl.ub2()

    def lrc(self):
        """
        Returns the reduced cost at lower bound.
        """
        return self._impl.lrc()

    def urc(self):
        """
        Returns the reduced cost at upper bound.
        """
        return self._impl.urc()

    def lslack(self):
        """
        Return the slack at lower bound (``val - lb``). See
        :ref:`secVariableSuffixesNotes`.
        """
        return self._impl.lslack()

    def uslack(self):
        """
        Return the slack at upper bound (``ub - val``). See
        :ref:`secVariableSuffixesNotes`.
        """
        return self._impl.uslack()

    def rc(self):
        """
        Get the reduced cost (at the nearer bound).
        """
        return self._impl.rc()

    def slack(self):
        """
        Returns the bound slack which is the lesser of
        :func:`~amplpy.Variable.lslack` and :func:`~amplpy.Variable.uslack`.
        See :ref:`secVariableSuffixesNotes`.
        """
        return self._impl.slack()

    def sstatus(self):
        """
        Solver status (basis status of variable).
        """
        return self._impl.sstatus()

    def status(self):
        """
        AMPL status if not `in`, otherwise solver status.
        """
        return self._impl.status()


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

    An LogicError is thrown if one of such methods is called for
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
        self._impl.isLogical()

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
        A possible workaround is to set the option `presolve` to `false`
        (see :func:`~amplpy.AMPL.setOption`).

        Args:
            dual: The value to be assigned to the dual variable.
        """
        self._impl.setDual(dual)

    def val(self):
        """
        Get the AMPL val suffix. Valid only for logical constraints.
        """
        return self._impl.val()
