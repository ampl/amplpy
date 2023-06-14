# -*- coding: utf-8 -*-


def display_error_message(exception, error=True):
    msg = "\t" + str(exception).replace("\n", "\n\t")
    if error:
        print("Error:\n{:s}".format(msg))
    else:
        print("Warning:\n{:s}".format(msg))


class ErrorHandler:
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
