# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from .entity import Entity


class Objective(Entity):
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
    suffixes for that entities), see :func:`~amplpy.Entity.getValues` and the
    :class:`~amplpy.DataFrame` class.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, Objective)

    def value(self):
        """
        Get the value of the objective.
        """
        return self._impl.value()

    def astatus(self):
        """
        Return the AMPL status.
        """
        return self._impl.astatus()

    def sstatus(self):
        """
        Return the solver status.
        """
        return self._impl.sstatus()

    def exitcode(self):
        """
        Exit code returned by solver after most recent solve with this
        objective.
        """
        return self._impl.exitcode()

    def message(self):
        """
        Result message returned by solver after most recent solve with this
        objective.
        """
        return self._impl.message()

    def result(self):
        """
        Result string returned by solver after most recent solve with this
        objective.
        """
        return self._impl.result()

    def drop(self):
        """
        Drop this objective instance.
        """
        self._impl.drop()

    def restore(self):
        """
        Restore this objective (if it had been dropped, no effect otherwise).
        """
        self._impl.restore()

    def minimization(self):
        """
        Get the sense of this objective. Returns True if minimize,
        False if maximize.
        """
        return self._impl.minimization()
