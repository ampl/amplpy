# -*- coding: utf-8 -*-
try:
    from .tools import _SUPPORT_MESSAGE
except Exception:
    _SUPPORT_MESSAGE = ""

def display_error_message(exception, error=True):
    msg = "\t" + str(exception).replace("\n", "\n\t")
    if error:
        print(f"Error:\n{msg}{_SUPPORT_MESSAGE}")
    else:
        print(f"Warning:\n{msg}")


cdef class ErrorHandler:
    """
    A basic interface for AMPL error handlers. If an application needs to
    implement customized error handling, it must implement this interface and
    then register an instance with the AMPL API using the
    :func:`~amplpy.AMPL.set_error_handler` method.
    The underlying AMPL interpreter will then report all errors and warnings
    through this interface as :class:`~amplpy.AMPLException` objects.
    """

    def error(self, exception):
        """
        Receives notification of an error.
        """
        display_error_message(exception)
        raise exception

    def warning(self, exception):
        """
        Receives notification of a warning.
        """
        display_error_message(exception, error=False)

cdef void PyError(bool_c isWarning, const char* filename, int row, int offset, const char* message, void* errorHandler) except * with gil:
    handler = <ErrorHandler>errorHandler
    exception = AMPLException(filename.decode('utf-8'), row, offset, message.decode('utf-8'))
    if isWarning:
        handler.warning(exception)
    else:
        handler.error(exception)
