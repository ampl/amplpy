# https://cython.readthedocs.io/en/latest/src/tutorial/clibraries.html
from campl cimport *

include "base.pxi"
include "entity.pxi"

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
    cdef AMPLPtr* _c_ampl

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
        res = AMPL_Create(&self._c_ampl)
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
        AMPL_Eval(self._c_ampl, statements.encode('utf-8'))

    def reset(self):
        """
        Clears all entities in the underlying AMPL interpreter, clears all maps
        and invalidates all entities.
        """
        AMPL_Reset(self._c_ampl)

    def close(self):
        """
        Stops the underlying engine, and release all any further attempt to
        execute optimization commands without restarting it will throw an
        exception.
        """
        if self._c_ampl is not NULL:
            AMPL_Close(self._c_ampl)
            AMPL_Destroy(&self._c_ampl);
            self._c_ampl = NULL

    def __dealloc__(self):
        self.close()

















    def get_output(self, statements):
        """
        Equivalent to :func:`~amplpy.AMPL.eval` but returns the output as a
        string.

        Args:
          statements: A collection of AMPL statements and declarations to
          be passed to the interpreter.

        Returns:
          A string with the output.
        """
        # Workaround for #56
        if not statements.endswith((" ", ";", "\n")):
            statements += "\n"
        cdef char* output_c
        AMPL_GetOutput(self._c_ampl, statements.encode('utf-8'), &output_c)
        output = str(output_c.decode('utf-8'))
        AMPL_StringFree(output_c)
        return output

    def is_running(self):
        """
        Returns true if the underlying engine is running.
        """
        cdef bool isrunning
        AMPL_IsRunning(self._c_ampl, &isrunning)
        return isrunning

    def solve(self, problem="", solver="", verbose=True, return_output=False, **kwargs):
        """
        Solve the current model or the problem specified by ``problem``.

        Args:
            problem: Name of the problem to solve.

            solver: Name of the solver to use.

            verbose: Display verbose output if set to ``True``.

            return_output: Return output as a string if set to ``True``.

            kwargs: Pass ``solvername_options`` as additional arguments.

        Raises:
            RuntimeError: if the underlying interpreter is not running.
        """
        cdef char* output_c
        if not verbose or return_output:
            if solver is not None:
                AMPL_SetOption(self._c_ampl, "solver", solver.encode('utf-8'))
            for option, value in kwargs.items():
                assert option.endswith("_options")
                AMPL_SetOption(self._c_ampl, option.encode('utf-8'), value.encode('utf-8'))
            if problem is None:
                AMPL_GetOutput(self._c_ampl, "solve;", &output_c)
            else:
                AMPL_GetOutput(self._c_ampl, f"solve {problem};", &output_c)
            output = str(output_c.decode('utf-8'))
            AMPL_StringFree(output_c)
            if return_output:
                return output
        else:
            AMPL_Solve(self._c_ampl, problem.encode('utf-8'), solver.encode('utf-8'))

    def cd(self, path=None):
        """
        Get or set the current working directory from the underlying
        interpreter (see https://en.wikipedia.org/wiki/Working_directory).

        Args:
            path: New working directory or None (to display the working
            directory).

        Returns:
            Current working directory.
        """
        cdef char* workdir_c
        if path is None:
            AMPL_Cd(self._c_ampl, &workdir_c)
        else:
            AMPL_Cd2(self._c_ampl, path.encode('utf-8'), &workdir_c)
        workdir = str(workdir_c.decode('utf-8'))
        AMPL_StringFree(workdir_c)
        return workdir

    def set_option(self, name, value):
        """
        Set an AMPL option to a specified value.

        Args:
            name: Name of the option to be set (alphanumeric without spaces).

            value: The value the option must be set to.

        Raises:
            InvalidArgumet: if the option name is not valid.

            TypeError: if the value has an invalid type.
        """
        #if isinstance(value, bool):
        #    AMPL_SetDblOption(self._c_ampl, name.encode('utf-8'), value)
        #elif isinstance(value, int):
        if isinstance(value, int):
            AMPL_SetDblOption(self._c_ampl, name.encode('utf-8'), value)
        elif isinstance(value, float):
            AMPL_SetDblOption(self._c_ampl, name.encode('utf-8'), value)
        elif isinstance(value, str):
            AMPL_SetOption(self._c_ampl, name.encode('utf-8'), value.encode('utf-8'))
        else:
            raise TypeError

    def read(self, filename):
        """
        Interprets the specified file (script or model or mixed) As a side
        effect, it invalidates all entities (as the passed file can contain any
        arbitrary command); the lists of entities will be re-populated lazily
        (at first access).

        Args:
            filename: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        AMPL_Read(self._c_ampl, str(filename).encode('utf-8'))

    def read_data(self, filename):
        """
        Interprets the specified file as an AMPL data file. As a side effect,
        it invalidates all entities (as the passed file can contain any
        arbitrary command); the lists of entities will be re-populated lazily
        (at first access). After reading the file, the interpreter is put back
        to "model" mode.

        Args:
            filename: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        AMPL_ReadData(self._c_ampl, str(filename).encode('utf-8'))










    def read_table(self, table_name):
        """
        Read the table corresponding to the specified name, equivalent to the
        AMPL statement:

        .. code-block:: ampl

            read table table_name;

        Args:
            table_name: Name of the table to be read.
        """
        AMPL_ReadTable(self._c_ampl, table_name.encode('utf-8'))

    def write_table(self, table_name):
        """
        Write the table corresponding to the specified name, equivalent to the
        AMPL statement

        .. code-block:: ampl

            write table table_name;

        Args:
            table_name: Name of the table to be written.
        """
        AMPL_WriteTable(self._c_ampl, table_name.encode('utf-8'))





    def export_model(self, filename=""):
        """
        Create a .mod file with the model that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        cdef char* output_c
        AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), 1, 0, 0, &output_c)
        output = str(output_c.decode('utf-8'))
        AMPL_StringFree(output_c)
        return output

    def export_data(self, filename=""):
        """
        Create a .dat file with the data that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        cdef char* output_c
        AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), 0, 1, 0, &output_c)
        output = str(output_c.decode('utf-8'))
        AMPL_StringFree(output_c)
        return output

    def snapshot(self, filename="", model=True, data=True, options=True):
        """
        Create a snapshot file that replicates the current session.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).

            model: include model declaration if set to ``True``.

            data: include data declaration if set to ``True``.

            options: include options if set to ``True``.
        """
        cdef int model_c = model
        cdef int data_c = data
        cdef int options_c = options
        cdef char* output_c
        AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), model_c, data_c, options_c, &output_c)
        output = str(output_c.decode('utf-8'))
        AMPL_StringFree(output_c)
        return output








    def _start_recording(self, filename):
        """
        Start recording the session to a file for debug purposes.
        """
        filename = str(filename)
        AMPL_SetOption(self._c_ampl, "_log_file_name", filename.encode('utf-8'))
        AMPL_SetDblOption(self._c_ampl, "_log_input_only", 1)
        AMPL_SetDblOption(self._c_ampl, "_log", 1)

    def _stop_recording(self):
        """
        Stop recording the session.
        """
        AMPL_SetDblOption(self._c_ampl, "_log", 0)
