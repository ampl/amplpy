# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from . import amplpython


class ErrorHandler:
    """
    A basic interface for AMPL error handlers. If an application needs to
    implement customised error handling, it must implement this interface and
    then register an instance with the AMPL API using the
    :func:`~amplpy.AMPL.setErrorHandler` method. The underlying AMPL
    interpreter will then report all errors and warnings through this
    interface as :class:`~amplpy.AMPLException` objects.
    """
    def error(self, amplexception):
        """
        Receives notification of an error.
        """
        msg = '\t'+str(amplexception).replace('\n', '\n\t')
        print('Error:\n{:s}'.format(msg))
        raise amplexception

    def warning(self, amplexception):
        """
        Receives notification of a warning.
        """
        msg = '\t'+str(amplexception).replace('\n', '\n\t')
        print('Warning:\n{:s}'.format(msg))
