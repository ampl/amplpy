# https://cython.readthedocs.io/en/latest/src/tutorial/clibraries.html
cimport campl

cdef class AMPL:
    """An AMPL translator.

    An object of this class can be used to do the following tasks:

    - Run AMPL code. See :func:`~amplpy.AMPL.eval`.
    - Read models and data from files. See :func:`~amplpy.AMPL.read`,
      :func:`~amplpy.AMPL.read_data`.
    - Solve optimization problems constructed from model and data (see
      :func:`~amplpy.AMPL.solve`).
    - Access single Elements of an optimization problem. See
      :func:`~amplpy.AMPL.get_variable`,
      :func:`~amplpy.AMPL.get_constraint`,
      :func:`~amplpy.AMPL.get_objective`,
      :func:`~amplpy.AMPL.get_set`,
      and :func:`~amplpy.AMPL.get_parameter`.
    - Access lists of available entities of an optimization problem. See
      :func:`~amplpy.AMPL.get_variables`,
      :func:`~amplpy.AMPL.get_constraints`,
      :func:`~amplpy.AMPL.get_objectives`,
      :func:`~amplpy.AMPL.get_sets`,
      and :func:`~amplpy.AMPL.get_parameters`.

    Error handling is two-faced:

    - Errors coming from the underlying AMPL translator (e.g. syntax errors and
      warnings obtained calling the eval method) are handled by
      the :class:`~amplpy.ErrorHandler` which can be set and get via
      :func:`~amplpy.AMPL.get_error_handler` and
      :func:`~amplpy.AMPL.set_error_handler`.
    - Generic errors coming from misusing the API, which are detected in
      Python, are thrown as exceptions.

    The default implementation of the error handler throws exceptions on errors
    and prints to console on warnings.

    The output of every user interaction with the underlying translator is
    handled implementing the abstract class :class:`~amplpy.OutputHandler`.
    The (only) method is called at each block of output from the translator.
    The current output handler can be accessed and set via
    :func:`~amplpy.AMPL.get_output_handler` and
    :func:`~amplpy.AMPL.set_output_handler`.
    """
    cdef campl.AMPLPtr* _c_ampl

    def __cinit__(self, environment=None):
        """
        Constructor:
        creates a new AMPL instance with the specified environment if provided.

        Args:
            environment (:class:`~amplpy.Environment`): This allows the user to
            specify the location of the AMPL binaries to be used and to modify
            the environment variables in which the AMPL interpreter will run.

        Raises:
            RuntimeError: If no valid AMPL license has been found or if the
            translator cannot be started for any other reason.
        """
        res = campl.AMPL_Create(&self._c_ampl)
        assert res == 0

    def eval(self, statements):
        """
        Parses AMPL code and evaluates it as a possibly empty sequence of AMPL
        declarations and statements.

        As a side effect, it invalidates all entities (as the passed statements
        can contain any arbitrary command); the lists of entities will be
        re-populated lazily (at first access)

        The output of interpreting the statements is passed to the current
        OutputHandler (see getOutputHandler and
        setOutputHandler).

        By default, errors and warnings are printed on stdout.
        This behavior can be changed reassigning an ErrorHandler
        using setErrorHandler.

        Args:
          statements: A collection of AMPL statements and declarations to
          be passed to the interpreter.

        Raises:
          RuntimeError: if the input is not a complete AMPL statement (e.g.
          if it does not end with semicolon) or if the underlying
          interpreter is not running.
        """
        # Workaround for #56
        if not statements.endswith((" ", ";", "\n")):
            statements += "\n"
        campl.AMPL_Eval(self._c_ampl, statements.encode('utf-8'))

    def reset(self):
        """
        Clears all entities in the underlying AMPL interpreter, clears all maps
        and invalidates all entities.
        """
        campl.AMPL_Reset(self._c_ampl)

    def close(self):
        """
        Stops the underlying engine, and release all any further attempt to
        execute optimization commands without restarting it will throw an
        exception.
        """
        if self._c_ampl is not NULL:
            campl.AMPL_Close(self._c_ampl)
            campl.AMPL_Destroy(&self._c_ampl);
            self._c_ampl = NULL

    def __dealloc__(self):
        self.close()
