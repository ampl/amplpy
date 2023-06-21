# -*- coding: utf-8 -*-
from numbers import Real

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

    All these methods throw a TypeError if called for a non scalar
    objective and an RuntimeError if called on an entity which has been deleted
    in the underlying intepreter.

    To gain access to all the values in an entity (for all instances and all
    suffixes for that entities), see
    :func:`~amplpy.Entity.get_values`
    and the :class:`~amplpy.DataFrame` class.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, Variable)

    def __setitem__(self, index, value):
        self.__getitem__(index).set_value(value)

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
            self._impl.fix(float(value))

    def unfix(self):
        """
        Unfix all instances of this variable.
        """
        self._impl.unfix()

    def set_value(self, value):
        """
        Set the current value of this variable (does not fix it),
        equivalent to the AMPL command `let`.

        Args:
            value: value to be set.
        """
        self._impl.setValue(float(value))

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
        Returns the current lower bound.
        """
        return self._impl.lb()

    def ub(self):
        """
        Returns the current upper bound.
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
        Return the slack at lower bound (``val - lb``).
        """
        return self._impl.lslack()

    def uslack(self):
        """
        Return the slack at upper bound (``ub - val``).
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

    # Aliases
    setValue = set_value
