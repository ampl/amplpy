# -*- coding: utf-8 -*-
import logging

try:
    from .tools import _SUPPORT_MESSAGE
except Exception:
    _SUPPORT_MESSAGE = ""

logger = logging.getLogger("amplpy")
logger.setLevel(logging.WARNING)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

def display_error_message(exception, error=True):
    logger.setLevel(logging.WARNING)
    msg = "\t" + str(exception).replace(_SUPPORT_MESSAGE, "").replace("\n", "\n\t")
    if error:
        logger.error(f"\n{msg}")
    else:
        logger.warning(f"\n{msg}")


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
        raise exception

cdef void PyError(bool_c isWarning, const char* filename, int row, int offset, const char* message, void* errorHandler) except * with gil:
    handler = <ErrorHandler>errorHandler
    if isWarning:
        exception = AMPLException(filename.decode('utf-8'), row, offset, message.decode('utf-8'))
        handler.warning(exception)
    else:
        exception = AMPLException(filename.decode('utf-8'), row, offset, f"{message.decode('utf-8')}{_SUPPORT_MESSAGE}")
        handler.error(exception)
