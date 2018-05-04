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

    def __init__(self):
        self.error_count = 0
        self.warning_count = 0
        self.last_error = None
        self.last_warning = None

    def reset(self):
        """
        Resets error and warning counts.
        """
        self.error_count = 0
        self.warning_count = 0

    def check(self):
        """
        Raises an exception if there has been an error.
        """
        if self.error_count != 0:
            raise RuntimeError('Errors: {}; Warnings: {}'.format(
                    self.error_count, self.warning_count))

    def error(self, amplexception):
        """
        Receives notification of an error.
        """
        self.last_error = amplexception.getMessage()
        print('Error:', self.last_error)

    def warning(self, amplexception):
        """
        Receives notification of a warning.
        """
        self.last_warning = amplexception.getMessage()
        print('Warning:', self.last_warning)
