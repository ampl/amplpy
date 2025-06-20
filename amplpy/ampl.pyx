# https://cython.readthedocs.io/en/latest/src/tutorial/clibraries.html
import sys

cimport amplpy.campl as campl

from libc.stdlib cimport malloc, free
from libc.string cimport strdup

from cpython.bool cimport PyBool_Check

from cpython cimport Py_INCREF, Py_DECREF

import builtins

from numbers import Real
from ast import literal_eval

include "util.pxi" # must be first
include "constraint.pxi"
include "dataframe.pxi"
include "entity.pxi"
include "environment.pxi"
include "errorhandler.pxi"
include "exceptions.pxi"
include "iterators.pxi"
include "objective.pxi"
include "outputhandler.pxi"
include "parameter.pxi"
include "set.pxi"
include "variable.pxi"


def nested_dict_of_suffixes(lst):
    nested = {}
    for name, value in lst:
        if "[" not in name:
            nested[name] = value
        else:
            p = name.find("[")
            v, index = name[:p], literal_eval(f"({name[p+1:-1]},)")
            if v not in nested:
                nested[v] = {}
            if len(index) == 1:
                index = index[0]
            nested[v][index] = value
    return nested


AMPL_NOT_FOUND_MESSAGE = """
Please make sure that the AMPL directory is in the system search path, or
add it before instantiating the AMPL object with:

    from amplpy import AMPL, add_to_path
    add_to_path(r"full path to the AMPL installation directory")
    ampl = AMPL()

Or, if you are using amplpy.modules, please make sure that they are installed:

    # Install solver modules (e.g., HiGHS, CBC, Gurobi)
    $ python -m amplpy.modules install highs cbc gurobi
"""

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
    cdef campl.AMPL* _c_ampl
    cdef object _output_handler
    cdef object _error_handler
    cdef object _error_handler_wrapper

    def __init__(self, environment=None):
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
        cdef Environment env
        try:
            if environment is None and os.name == "nt":
                environment = Environment()
            if environment is None:
                PY_AMPL_CALL(campl.AMPL_Create(&self._c_ampl))
            else:
                env = environment
                PY_AMPL_CALL(campl.AMPL_CreateWithEnv(&self._c_ampl, env.get_c_pointer()))
        except RuntimeError as exp:
            if str(exp).startswith("AMPL could not be started"):
                print("*" * 79, file=sys.stderr)
                for line in AMPL_NOT_FOUND_MESSAGE.split("\n"):
                    print(f"* {line:75} *", file=sys.stderr)
                print("*" * 79, file=sys.stderr)
            raise
        self._output_handler = None
        self._error_handler = None
        self.set_output_handler(OutputHandler())
        self.set_error_handler(ErrorHandler())

    def __dealloc__(self):
        """
        Default destructor:
        releases all the resources related to the AMPL instance (most notably
        kills the underlying  interpreter).
        """
        self.close()

    def get_data(self, *statements):
        """
        Get the data corresponding to the display statements. The statements
        can be AMPL expressions, or entities. It captures the equivalent of the
        command:

        .. code-block:: ampl

            display ds1, ..., dsn;

        where ds1, ..., dsn are the ``displayStatements`` with which the
        function is called.

        As only one DataFrame is returned, the operation will fail if the
        results of the display statements cannot be indexed over the same set.
        As a result, any attempt to get data from more than one set, or to get
        data for multiple parameters with a different number of indexing sets
        will fail.

        Args:
            statements: The display statements to be fetched.

        Raises:
            TypeError: if the AMPL visualization command does not succeed
            for one of the reasons listed above.

            RuntimeError: if there are issues with the data.

        Returns:
            DataFrame capturing the output of the display
            command in tabular form.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_DATAFRAME* data
        cdef char** statements_c = <char**> malloc(len(statements) * sizeof(char*))
        for i in range(len(statements)):
            statements_c[i] = strdup(statements[i].encode('utf-8'))
        errorinfo = campl.AMPL_GetData(self._c_ampl, statements_c, len(statements), &data)
        for i in range(len(statements)):
            free(statements_c[i])
        free(statements_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        return DataFrame.create(data)

    def get_entity(self, name):
        """
        Get entity corresponding to the specified name (looks for it in all
        types of entities).

        Args:
            name: Name of the entity.

        Raises:
            KeyError: if the specified entity does not exist.

        Returns:
            The AMPL entity with the specified name.
        """
        cdef char* name_c = strdup(name.encode('utf-8'))
        return Entity.create(self, name_c, NULL, None)

    def get_variable(self, name):
        """
        Get the variable with the corresponding name.

        Args:
            name: Name of the variable to be found.

        Raises:
            KeyError: if the specified variable does not exist.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(name.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != campl.AMPL_VARIABLE:
            free(name_c)
            raiseKeyError(campl.AMPL_VARIABLE, name)
        return Variable.create(self, name_c, NULL, None)

    def get_constraint(self, name):
        """
        Get the constraint with the corresponding name.

        Args:
            name: Name of the constraint to be found.

        Raises:
            KeyError: if the specified constraint does not exist.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(name.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != campl.AMPL_CONSTRAINT:
            free(name_c)
            raiseKeyError(campl.AMPL_CONSTRAINT, name)
        return Constraint.create(self, name_c, NULL, None)

    def get_objective(self, name):
        """
        Get the objective with the corresponding name.

        Args:
            name: Name of the objective to be found.

        Raises:
            KeyError: if the specified objective does not exist.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(name.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != campl.AMPL_OBJECTIVE:
            free(name_c)
            raiseKeyError(campl.AMPL_OBJECTIVE, name)
        return Objective.create(self, name_c, NULL, None)

    def get_set(self, name):
        """
        Get the set with the corresponding name.

        Args:
            name: Name of the set to be found.

        Raises:
            KeyError: if the specified set does not exist.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(name.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != campl.AMPL_SET:
            free(name_c)
            raiseKeyError(campl.AMPL_SET, name)
        return Set.create(self, name_c, NULL, None)

    def get_parameter(self, name):
        """
        Get the parameter with the corresponding name.

        Args:
            name: Name of the parameter to be found.

        Raises:
            KeyError: if the specified parameter does not exist.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_ENTITYTYPE entitytype
        cdef char* name_c = strdup(name.encode('utf-8'))
        errorinfo = campl.AMPL_EntityGetType(self._c_ampl, name_c, &entitytype)
        if errorinfo:
            free(name_c)
            PY_AMPL_CALL(errorinfo)
        if entitytype != campl.AMPL_PARAMETER:
            free(name_c)
            raiseKeyError(campl.AMPL_PARAMETER, name)
        return Parameter.create(self, name_c, NULL, None)

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
        PY_AMPL_CALL(campl.AMPL_Eval(self._c_ampl, statements.encode('utf-8')))
        self._error_handler_wrapper.check()

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
        PY_AMPL_CALL(campl.AMPL_GetOutput(self._c_ampl, statements.encode('utf-8'), &output_c))
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)
        return output

    def reset(self):
        """
        Clears all entities in the underlying AMPL interpreter, clears all maps
        and invalidates all entities.
        """
        PY_AMPL_CALL(campl.AMPL_Reset(self._c_ampl))

    def close(self):
        """
        Stops the underlying engine, and release all any further attempt to
        execute optimization commands without restarting it will throw an
        exception.
        """
        if self._c_ampl is not NULL:
            PY_AMPL_CALL(campl.AMPL_Close(self._c_ampl))
            campl.AMPL_Free(&self._c_ampl);
            self._c_ampl = NULL

    def is_running(self):
        """
        Returns true if the underlying engine is running.
        """
        cdef bool_c isrunning
        PY_AMPL_CALL(campl.AMPL_IsRunning(self._c_ampl, &isrunning))
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
        for option, value in kwargs.items():
            if option.endswith("_options"):
                self.set_option(option, value)
        if not verbose or return_output:
            if solver != "":
                self.set_option("solver", solver)
            output = self.get_output(f"solve {problem};")
            if return_output:
                return output
        else:
            PY_AMPL_CALL(campl.AMPL_Solve(self._c_ampl, problem.encode('utf-8'), solver.encode('utf-8')))

    def cd(self, path=None):
        """
        Get or set the current working directory from the underlying
        interpreter (see https://en.wikipedia.org/wiki/Working_directory).

        Args:
            path: New working directory or None (to display the working
            directory).

        Returns:
            Current working directory.

        Raises:
            RuntimeError: change directory cannot be executed.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* workdir_c
        if path is None:
            errorinfo = campl.AMPL_Cd(self._c_ampl, &workdir_c)
        else:
            errorinfo = campl.AMPL_Cd2(self._c_ampl, path.encode('utf-8'), &workdir_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        workdir = str(workdir_c.decode('utf-8'))
        campl.AMPL_StringFree(&workdir_c)

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
        if PyBool_Check(value):
            PY_AMPL_CALL(campl.AMPL_SetBoolOption(self._c_ampl, name.encode('utf-8'), value))
        elif isinstance(value, int):
            PY_AMPL_CALL(campl.AMPL_SetDblOption(self._c_ampl, name.encode('utf-8'), value))
        elif isinstance(value, float):
            PY_AMPL_CALL(campl.AMPL_SetDblOption(self._c_ampl, name.encode('utf-8'), value))
        elif isinstance(value, str):
            PY_AMPL_CALL(campl.AMPL_SetOption(self._c_ampl, name.encode('utf-8'), value.encode('utf-8')))
        else:
            raise TypeError

    def get_option(self, name):
        """
        Get the current value of the specified option. If the option does not
        exist, returns None.

        Args:
            name: Option name.

        Returns:
            Value of the option.

        Raises:
            InvalidArgumet: if the option name is not valid.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef bool_c exists
        cdef char* value_c

        errorinfo = campl.AMPL_GetOption(self._c_ampl, name.encode('utf-8'), &exists, &value_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

        value = value_c.decode('utf-8')
        campl.AMPL_StringFree(&value_c)
        if exists:
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value

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
        PY_AMPL_CALL(campl.AMPL_Read(self._c_ampl, str(filename).encode('utf-8')))
        self._error_handler_wrapper.check()

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
        PY_AMPL_CALL(campl.AMPL_ReadData(self._c_ampl, str(filename).encode('utf-8')))
        self._error_handler_wrapper.check()

    def get_value(self, scalar_expression):
        """
        Get a scalar value from the underlying AMPL interpreter, as a double or
        a string.

        Args:
            scalar_expression: An AMPL expression which evaluates to a scalar
            value.

        Returns:
            The value of the expression.

        Raises:
            TypeError: in case scalar_expression does not evaluate to a value.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef campl.AMPL_VARIANT* v
        errorinfo = campl.AMPL_GetValue(self._c_ampl, scalar_expression.encode('utf-8'), &v)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

        py_variant = to_py_variant(v)
        campl.AMPL_VariantFree(&v)

        return py_variant

    def set_data(self, data, set_name=None):
        """
        Assign the data in the dataframe to the AMPL entities with the names
        corresponding to the column names.

        Args:
            data: The dataframe containing the data to be assigned.

            set_name: The name of the set to which the indices values of the
            DataFrame are to be assigned.

        Raises:
            AMPLException: if the data assignment procedure was not successful.
        """
        if not isinstance(data, DataFrame):
            if pd is not None and isinstance(data, (pd.DataFrame, pd.Series)):
                data = DataFrame.from_pandas(data)
        cdef DataFrame data_frame = data
        cdef campl.AMPL_DATAFRAME* data_c = data_frame.get_ptr()
        if set_name is None:
            PY_AMPL_CALL(campl.AMPL_SetData(self._c_ampl, data_c, ""))
        else:
            PY_AMPL_CALL(campl.AMPL_SetData(self._c_ampl, data_c, set_name.encode('utf-8')))

    def read_table(self, table_name):
        """
        Read the table corresponding to the specified name, equivalent to the
        AMPL statement:

        .. code-block:: ampl

            read table table_name;

        Args:
            table_name: Name of the table to be read.
        """
        PY_AMPL_CALL(campl.AMPL_ReadTable(self._c_ampl, table_name.encode('utf-8')))

    def write_table(self, table_name):
        """
        Write the table corresponding to the specified name, equivalent to the
        AMPL statement

        .. code-block:: ampl

            write table table_name;

        Args:
            table_name: Name of the table to be written.
        """
        PY_AMPL_CALL(campl.AMPL_WriteTable(self._c_ampl, table_name.encode('utf-8')))

    def display(self, *ampl_expressions):
        """
        Writes on the current OutputHandler the outcome of the AMPL statement.

        .. code-block:: ampl

            display e1, e2, .., en;

        where e1, ..., en are the strings passed to the procedure.

        Args:
            ampl_expressions: Expressions to be evaluated.

        Raises:
            RuntimeError: if ampl_expressions do not evaluate to expressions.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        exprs = list(map(str, ampl_expressions))
        cdef int size = len(exprs)
        cdef const char** array = <const char**>malloc(size * sizeof(const char*))
    
        for i in range(size):
            array[i] = strdup(exprs[i].encode('utf-8'))
    
        display = "display"
        errorinfo = campl.AMPL_CallVisualisationCommandOnNames(self._c_ampl, display.encode('utf-8'), <const char* const*>array, size)
        for i in range(size):
            free(array[i])
        free(array)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)

    def set_output_handler(self, output_handler):
        """
        Sets a new output handler.

        Args:
            output_handler: The function handling the AMPL output derived from
            interpreting user commands.
        """
        self._output_handler = output_handler
        PY_AMPL_CALL(campl.AMPL_SetOutputHandler(self._c_ampl, PyOutput, <void*>output_handler))

    def set_error_handler(self, error_handler):
        """
        Sets a new error handler.

        Args:
            error_handler: The object handling AMPL errors and warnings.
        """
        class ErrorHandlerWrapper(ErrorHandler):
            def __init__(self, ampl_instance, error_handler):
                self.ampl = ampl_instance
                self.error_handler = error_handler
                self.last_exception = None

            def error(self, exception):
                try:
                    self.error_handler.error(exception)
                except Exception as exp:
                    if self.last_exception is None:
                        self.last_exception = exp

            def warning(self, exception):
                try:
                    self.error_handler.warning(exception)
                except Exception as exp:
                    if self.last_exception is None:
                        if self.ampl.get_option("_throw_on_warnings") != 1.0:
                            pass
                        else:
                            self.last_exception = exp

            def check(self):
                if isinstance(self.last_exception, Exception):
                    exp = self.last_exception
                    self.last_exception = None
                    raise exp

        error_handler_wrapper = ErrorHandlerWrapper(self, error_handler)

        self._error_handler = error_handler
        self._error_handler_wrapper = error_handler_wrapper

        PY_AMPL_CALL(campl.AMPL_SetErrorHandler(self._c_ampl, PyError, <void*>self._error_handler_wrapper))

    def get_output_handler(self):
        """
        Get the current output handler.

        Returns:
            The current output handler.
        """
        cdef void* output_handler
        PY_AMPL_CALL(campl.AMPL_GetOutputHandler(self._c_ampl, &output_handler))
        return <OutputHandler>output_handler

    def get_error_handler(self):
        """
        Get the current error handler.

        Returns:
            The current error handler.
        """
        return <ErrorHandler>self._error_handler

    def get_variables(self):
        """
        Get all the variables declared.
        """
        return EntityMap.create(self, campl.AMPL_VARIABLE)

    def get_constraints(self):
        """
        Get all the constraints declared.
        """
        return EntityMap.create(self, campl.AMPL_CONSTRAINT)

    def get_objectives(self):
        """
        Get all the objectives declared.
        """
        return EntityMap.create(self, campl.AMPL_OBJECTIVE)

    def get_sets(self):
        """
        Get all the sets declared.
        """
        return EntityMap.create(self, campl.AMPL_SET)

    def get_parameters(self):
        """
        Get all the parameters declared.
        """
        return EntityMap.create(self, campl.AMPL_PARAMETER)

    def get_current_objective(self):
        """
        Get the the current objective. Returns `None` if no objective is set.
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* objname_c
        errorinfo = campl.AMPL_GetCurrentObjective(self._c_ampl, &objname_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        objname = str(objname_c.decode('utf-8'))
        campl.AMPL_StringFree(&objname_c)
        if objname == "":
            return None
        else:
            return self.get_objective(objname)

    def _var(self):
        """
        Get/Set a variable.
        """

        class Variables(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_variable(name)

            def __setitem__(self, name, value):
                if isinstance(value, Real):
                    self.ampl.get_variable(name).set_value(value)
                else:
                    self.ampl.get_variable(name).set_values(value)

            def __iter__(self):
                return self.ampl.get_variables()

        return Variables(self)

    def _con(self):
        """
        Get/Set a constraint.
        """

        class Constraints(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_constraint(name)

            def __setitem__(self, name, value):
                if isinstance(value, Real):
                    self.ampl.get_constraint(name).set_dual(value)
                else:
                    self.ampl.get_constraint(name).set_values(value)

            def __iter__(self):
                return self.ampl.get_constraints()

        return Constraints(self)

    def _obj(self):
        """
        Get an objective.
        """

        class Objectives(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_objective(name)

            def __iter__(self):
                return self.ampl.get_objectives()

        return Objectives(self)

    def _set(self):
        """
        Get/Set a set.
        """

        class Sets(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_set(name)

            def __setitem__(self, name, values):
                self.ampl.get_set(name).set_values(values)

            def __iter__(self):
                return self.ampl.get_sets()

        return Sets(self)

    def _param(self):
        """
        Get/Set a parameter.
        """

        class Parameters(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_parameter(name)

            def __setitem__(self, name, value):
                if isinstance(value, (Real, str)):
                    self.ampl.get_parameter(name).set(value)
                else:
                    self.ampl.get_parameter(name).set_values(value)

            def __iter__(self):
                return self.ampl.get_parameters()

        return Parameters(self)

    def _option(self):
        """
        Get/Set an option.
        """

        class Options(object):
            def __init__(self, ampl):
                self.ampl = ampl

            def __getitem__(self, name):
                return self.ampl.get_option(name)

            def __setitem__(self, name, value):
                if isinstance(value, dict):
                    if name.endswith("_options"):
                        self.ampl.set_option(name, " ".join(f"{k}={int(v) if isinstance(v, builtins.bool) else v}" for k, v in value.items()))
                else:
                    self.ampl.set_option(name, value)

        return Options(self)

    def _set_option(self, options_dict):
        for name, value in options_dict.items():
            if isinstance(value, dict):
                if name.endswith("_options"):
                    self.set_option(name, " ".join(f"{k}={int(v) if isinstance(v, builtins.bool) else v}" for k, v in value.items()))
            else:
                self.set_option(name, value)

    var = property(_var)
    con = property(_con)
    obj = property(_obj)
    set = property(_set)
    param = property(_param)
    option = property(_option, _set_option)

    def export_model(self, filename=""):
        """
        Create a .mod file with the model that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* output_c
        errorinfo = campl.AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), 1, 0, 0, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)

        return output

    def export_data(self, filename=""):
        """
        Create a .dat file with the data that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* output_c
        errorinfo = campl.AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), 0, 1, 0, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)

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
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef int model_c = model
        cdef int data_c = data
        cdef int options_c = options
        cdef char* output_c
        errorinfo = campl.AMPL_Snapshot(self._c_ampl, filename.encode('utf-8'), model_c, data_c, options_c, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)

        return output

    def write(self, filename, auxfiles=""):
        """
        Invoke write command with filename as argument and
        set auxfiles if non-empty.

        Args:
            filename: outuput filename.
            auxfiles: auxfiles to export.
        """
        PY_AMPL_CALL(campl.AMPL_Write(self._c_ampl, filename.encode('utf-8'), auxfiles.encode('utf-8')))

    @property
    def solve_result(self):
        """
        Return solve_result value, which indicates if the problem has been solved.

        +---------+-----------+---------------------------------------------+
        | Number  |  String   |           Interpretation                    |
        +=========+===========+=============================================+
        |    0-99 |  solved   | Optimal solution found                      |
        +---------+-----------+---------------------------------------------+
        | 100-199 |  solved?  | Optimal solution indicated, but error likely|
        +---------+-----------+---------------------------------------------+
        | 200-299 | infeasible| Constraints cannot be satisfied             |
        +---------+-----------+---------------------------------------------+
        | 300-399 | unbounded | Objective can be improved without limit     |
        +---------+-----------+---------------------------------------------+
        | 400-499 |   limit   | Stopped by a limit that you set (such as on |
        |         |           | iterations)                                 |
        +---------+-----------+---------------------------------------------+
        | 500-599 |  failure  | Stopped by an error condition in the solver |
        |         |           | routines                                    |
        +---------+-----------+---------------------------------------------+
        """
        return self.get_value("solve_result")

    @property
    def solve_result_num(self):
        """
        Return solve_result_num value, which indicates if the problem has been solved.

        +---------+-----------+---------------------------------------------+
        | Number  |  String   |           Interpretation                    |
        +=========+===========+=============================================+
        |    0-99 |  solved   | Optimal solution found                      |
        +---------+-----------+---------------------------------------------+
        | 100-199 |  solved?  | Optimal solution indicated, but error likely|
        +---------+-----------+---------------------------------------------+
        | 200-299 | infeasible| Constraints cannot be satisfied             |
        +---------+-----------+---------------------------------------------+
        | 300-399 | unbounded | Objective can be improved without limit     |
        +---------+-----------+---------------------------------------------+
        | 400-499 |   limit   | Stopped by a limit that you set (such as on |
        |         |           | iterations)                                 |
        +---------+-----------+---------------------------------------------+
        | 500-599 |  failure  | Stopped by an error condition in the solver |
        |         |           | routines                                    |
        +---------+-----------+---------------------------------------------+
        """
        return self.get_value("solve_result_num")

    def get_iis(self, flat=True):
        """
        Get IIS attributes for all variables and constraints.

        Args:
            flat: Return flat dictionaries if set to True, or nested dictionaries otherwise.

        Returns:
            Tuple with a dictionary for variables in the IIS and another for the constraints.

        Usage example:

        .. code-block:: python

            from amplpy import AMPL
            ampl = AMPL()
            ampl.eval(
                r\"\"\"
            var x >= 0;
            var y >= 0;
            maximize obj: x+y;
            s.t. s: x+y <= -5;
            \"\"\"
            )
            ampl.option["presolve"] = 0  # disable AMPL presolve
            ampl.solve(solver="gurobi", gurobi_options="outlev=1 iis=1")
            if ampl.solve_result == "infeasible":
                var_iis, con_iis = ampl.get_iis()
                print(var_iis, con_iis)
        """
        iis_var = self.get_data(
            "{i in 1.._nvars: _var[i].iis != 'non'} (_varname[i], _var[i].iis)"
        ).to_list(skip_index=True)
        iis_con = self.get_data(
            "{i in 1.._ncons: _con[i].iis != 'non'} (_conname[i], _con[i].iis)"
        ).to_list(skip_index=True)
        if flat is False:
            iis_var = nested_dict_of_suffixes(iis_var)
            iis_con = nested_dict_of_suffixes(iis_con)
        else:
            iis_var = dict(iis_var)
            iis_con = dict(iis_con)
        return iis_var, iis_con

    def get_solution(self, flat=True, zeros=False):
        """
        Get solution values for all variables.

        Args:
            flat: Return a flat dictionary if set to True, or a nested dictionary otherwise.

            zeros: Include zeros in the solution if set to True.

        Returns:
            Returns a dictionary with the solution.

        Usage example:

        .. code-block:: python

            ampl.solve(solver="gurobi", gurobi_options="outlev=0")
            if ampl.solve_result == "solved":
                print(ampl.get_solution())
        """
        if zeros:
            stmt = "{i in 1.._nvars} (_varname[i], _var[i].val)"
        else:
            stmt = "{i in 1.._nvars: _var[i].val != 0} (_varname[i], _var[i].val)"
        lst_solution = self.get_data(stmt).to_list(skip_index=True)
        if flat:
            return dict(lst_solution)
        return nested_dict_of_suffixes(lst_solution)

    def _start_recording(self, filename):
        """
        Start recording the session to a file for debug purposes.
        """
        filename = str(filename)
        PY_AMPL_CALL(campl.AMPL_SetOption(self._c_ampl, "_log_file_name", filename.encode('utf-8')))
        PY_AMPL_CALL(campl.AMPL_SetDblOption(self._c_ampl, "_log_input_only", 1))
        PY_AMPL_CALL(campl.AMPL_SetDblOption(self._c_ampl, "_log", 1))

    def _stop_recording(self):
        """
        Stop recording the session.
        """
        PY_AMPL_CALL(campl.AMPL_SetDblOption(self._c_ampl, "_log", 0))

    def _load_session(self, filename):
        """
        Load a recorded session.
        """
        filename = str(filename)
        try:
            self.eval(open(filename).read())
        except RuntimeError as exp:
            print(exp)

    def to_ampls(self, driver, options=None):
        if driver == "gurobi":
            try:
                from amplpy_gurobi import export_gurobi_model
            except ImportError:
                raise ImportError("amplpy_gurobi package not found")
            return export_gurobi_model(self, options)
        elif driver == "cplex":
            try:
                from amplpy_cplex import export_cplex_model
            except ImportError:
                raise ImportError("amplpy_cplex package not found")
            return export_cplex_model(self, options)
        elif driver == "scip":
            try:
                from amplpy_scip import export_scip_model
            except ImportError:
                raise ImportError("amplpy_scip package not found")
            return export_scip_model(self, options)
        elif driver == "copt":
            try:
                from amplpy_copt import export_copt_model
            except ImportError:
                raise ImportError("amplpy_copt package not found")
            return export_copt_model(self, options)
        elif driver == "highs":
            try:
                from amplpy_highs import export_highs_model
            except ImportError:
                raise ImportError("amplpy_highs package not found")
            return export_highs_model(self, options)
        elif driver == "xpress":
            try:
                from amplpy_xpress import export_xpress_model
            except ImportError:
                raise ImportError("amplpy_xpress package not found")
            return export_xpress_model(self, options)
        solver_list = "copt, cplex, gurobi, highs, scip, xpress"
        raise ValueError(f"{driver} is not supported, please choose from: {solver_list}")

    def import_ampls_solution(self, model, number=None, import_entities=False, keep_files=False):
        if isinstance(model, dict):
            self.eval(
                "".join(
                    "let {} := {};".format(name, value) for name, value in model.items()
                )
            )
            return
        if isinstance(model, str):
            if number is None:
                self.eval(f'solution "{model}.sol";')
            else:
                self.eval(f'solution "{model}{number}.sol";')
            return
        import shutil
        model.write_sol()
        self.eval(f'solution "{model._solfile}";')
        if import_entities:
            self.eval(model.getRecordedEntities())
        if not keep_files:
            shutil.rmtree(model._tmpdir)

    def to_string(self):
        cdef campl.AMPL_ERRORINFO* errorinfo
        cdef char* output_c
        errorinfo = campl.AMPL_ToString(self._c_ampl, &output_c)
        if errorinfo:
            PY_AMPL_CALL(errorinfo)
        output = str(output_c.decode('utf-8'))
        campl.AMPL_StringFree(&output_c)
        
        return output

    def __str__(self):
        return self.to_string()

    # Aliases
    _loadSession = _load_session
    _startRecording = _start_recording
    _stopRecording = _stop_recording
    exportData = export_data
    exportModel = export_model
    getConstraint = get_constraint
    getConstraints = get_constraints
    getCurrentObjective = get_current_objective
    getData = get_data
    getEntity = get_entity
    getErrorHandler = get_error_handler
    getObjective = get_objective
    getObjectives = get_objectives
    getOption = get_option
    getOutput = get_output
    getOutputHandler = get_output_handler
    getParameter = get_parameter
    getParameters = get_parameters
    getSet = get_set
    getSets = get_sets
    getValue = get_value
    getVariable = get_variable
    getVariables = get_variables
    isRunning = is_running
    readData = read_data
    readTable = read_table
    setData = set_data
    setErrorHandler = set_error_handler
    setOption = set_option
    setOutputHandler = set_output_handler
    toString = to_string
    writeTable = write_table
