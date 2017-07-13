# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from . import amplpython


class Runnable(amplpython.Runnable):
    """
    Represent an object with only one function, which is called as a callback
    after an async execution has finished. Inherit from this class and use an
    instance in :func:`~amplpy.AMPL.evalAsync`, :func:`~amplpy.AMPL.readAsync`,
    :func:`~amplpy.AMPL.readDataAsync`, :func:`~amplpy.AMPL.solveAsync`.
    """

    def run(self):
        """
        Function called when the execution of the async operation is finished.
        """
        pass
