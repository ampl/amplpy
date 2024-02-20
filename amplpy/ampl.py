# -*- coding: utf-8 -*-
import sys
import os
from numbers import Real

from .errorhandler import ErrorHandler
from .outputhandler import OutputHandler
from .environment import Environment
from .objective import Objective
from .variable import Variable
from .constraint import Constraint
from .set import Set
from .parameter import Parameter
from .dataframe import DataFrame
from .iterators import EntityMap
from .entity import Entity
from . import exceptions
from . import amplpython

try:
    import pandas as pd
except ImportError:
    pd = None
inf = float("inf")


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


class AMPL(object):
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
        try:
            if environment is None and os.name == "nt":
                environment = Environment()
            if environment is None:
                self._impl = amplpython.AMPL()
            else:
                self._impl = amplpython.AMPL(environment._impl)
        except RuntimeError as exp:
            if str(exp).startswith("AMPL could not be started"):
                print("*" * 79, file=sys.stderr)
                for line in AMPL_NOT_FOUND_MESSAGE.split("\n"):
                    print(f"* {line:75} *", file=sys.stderr)
                print("*" * 79, file=sys.stderr)
            raise
        self._error_handler = None
        self._output_handler = None
        self.set_output_handler(OutputHandler())
        self.set_error_handler(ErrorHandler())

    def __del__(self):
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
        return DataFrame._from_data_frame_ref(
            self._impl.getData(list(statements), len(statements))
        )

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
        return Entity(self._impl.getEntity(name))

    def get_variable(self, name):
        """
        Get the variable with the corresponding name.

        Args:
            name: Name of the variable to be found.

        Raises:
            KeyError: if the specified variable does not exist.
        """
        return Variable(self._impl.getVariable(name))

    def get_constraint(self, name):
        """
        Get the constraint with the corresponding name.

        Args:
            name: Name of the constraint to be found.

        Raises:
            KeyError: if the specified constraint does not exist.
        """
        return Constraint(self._impl.getConstraint(name))

    def get_objective(self, name):
        """
        Get the objective with the corresponding name.

        Args:
            name: Name of the objective to be found.

        Raises:
            KeyError: if the specified objective does not exist.
        """
        return Objective(self._impl.getObjective(name))

    def get_set(self, name):
        """
        Get the set with the corresponding name.

        Args:
            name: Name of the set to be found.

        Raises:
            KeyError: if the specified set does not exist.
        """
        return Set(self._impl.getSet(name))

    def get_parameter(self, name):
        """
        Get the parameter with the corresponding name.

        Args:
            name: Name of the parameter to be found.

        Raises:
            KeyError: if the specified parameter does not exist.
        """
        return Parameter(self._impl.getParameter(name))

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
        self._impl.eval(statements)
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
        return self._impl.getOutput(statements)

    def reset(self):
        """
        Clears all entities in the underlying AMPL interpreter, clears all maps
        and invalidates all entities.
        """
        self._impl.reset()

    def close(self):
        """
        Stops the underlying engine, and release all any further attempt to
        execute optimization commands without restarting it will throw an
        exception.
        """
        try:
            self._impl.close()
        except AttributeError:
            pass

    def is_running(self):
        """
        Returns true if the underlying engine is running.
        """
        return self._impl.isRunning()

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
            self._impl.solve(problem, solver)

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
        if path is None:
            return self._impl.cd()
        return self._impl.cd(path)

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
        if isinstance(value, bool):
            self._impl.setBoolOption(name, value)
        elif isinstance(value, int):
            self._impl.setIntOption(name, value)
        elif isinstance(value, float):
            self._impl.setDblOption(name, value)
        elif isinstance(value, str):
            self._impl.setOption(name, value)
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
        try:
            value = self._impl.getOption(name).value()
        except RuntimeError:
            return None
        else:
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
        self._impl.read(str(filename))
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
        filename = str(filename)
        self._impl.readData(filename)
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
        """
        return self._impl.getValue(scalar_expression)

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
        if set_name is None:
            self._impl.setData(data._impl)
        else:
            self._impl.setData(data._impl, set_name)

    def read_table(self, table_name):
        """
        Read the table corresponding to the specified name, equivalent to the
        AMPL statement:

        .. code-block:: ampl

            read table table_name;

        Args:
            table_name: Name of the table to be read.
        """
        self._impl.readTable(table_name)

    def write_table(self, table_name):
        """
        Write the table corresponding to the specified name, equivalent to the
        AMPL statement

        .. code-block:: ampl

            write table table_name;

        Args:
            table_name: Name of the table to be written.
        """
        self._impl.writeTable(table_name)

    def display(self, *ampl_expressions):
        """
        Writes on the current OutputHandler the outcome of the AMPL statement.

        .. code-block:: ampl

            display e1, e2, .., en;

        where e1, ..., en are the strings passed to the procedure.

        Args:
            ampl_expressions: Expressions to be evaluated.
        """
        exprs = list(map(str, ampl_expressions))
        self._impl.displayLst(exprs, len(exprs))

    def set_output_handler(self, output_handler):
        """
        Sets a new output handler.

        Args:
            output_handler: The function handling the AMPL output derived from
            interpreting user commands.
        """

        class OutputHandlerInternal(amplpython.OutputHandler):
            def output(self, kind, msg):
                output_handler.output(kind, msg)

        self._output_handler = output_handler
        self._output_handler_internal = OutputHandlerInternal()
        self._impl.setOutputHandler(self._output_handler_internal)

    def set_error_handler(self, error_handler):
        """
        Sets a new error handler.

        Args:
            error_handler: The object handling AMPL errors and warnings.
        """

        class ErrorHandlerWrapper(ErrorHandler):
            def __init__(self, error_handler):
                self.error_handler = error_handler
                self.last_exception = None

            def error(self, exception):
                if isinstance(exception, amplpython.AMPLException):
                    exception = exceptions.AMPLException(exception)
                try:
                    self.error_handler.error(exception)
                except Exception as exp:
                    self.last_exception = exp

            def warning(self, exception):
                if isinstance(exception, amplpython.AMPLException):
                    exception = exceptions.AMPLException(exception)
                try:
                    self.error_handler.warning(exception)
                except Exception as exp:
                    self.last_exception = exp

            def check(self):
                if isinstance(self.last_exception, Exception):
                    exp = self.last_exception
                    self.last_exception = None
                    raise exp

        error_handler_wrapper = ErrorHandlerWrapper(error_handler)

        class InnerErrorHandler(amplpython.ErrorHandler):
            def error(self, exception):
                error_handler_wrapper.error(exception)

            def warning(self, exception):
                error_handler_wrapper.warning(exception)

        self._error_handler = error_handler
        self._error_handler_inner = InnerErrorHandler()
        self._error_handler_wrapper = error_handler_wrapper
        self._impl.setErrorHandler(self._error_handler_inner)

    def get_output_handler(self):
        """
        Get the current output handler.

        Returns:
            The current output handler.
        """
        return self._output_handler

    def get_error_handler(self):
        """
        Get the current error handler.

        Returns:
            The current error handler.
        """
        return self._error_handler

    def get_variables(self):
        """
        Get all the variables declared.
        """
        variables = self._impl.getVariables()
        return EntityMap(variables, Variable)

    def get_constraints(self):
        """
        Get all the constraints declared.
        """
        constraints = self._impl.getConstraints()
        return EntityMap(constraints, Constraint)

    def get_objectives(self):
        """
        Get all the objectives declared.
        """
        objectives = self._impl.getObjectives()
        return EntityMap(objectives, Objective)

    def get_sets(self):
        """
        Get all the sets declared.
        """
        sets = self._impl.getSets()
        return EntityMap(sets, Set)

    def get_parameters(self):
        """
        Get all the parameters declared.
        """
        parameters = self._impl.getParameters()
        return EntityMap(parameters, Parameter)

    def get_current_objective(self):
        """
        Get the the current objective. Returns `None` if no objective is set.
        """
        name = self._impl.getCurrentObjectiveName()
        if name == "":
            return None
        else:
            return self.get_objective(name)

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
                self.ampl.get_constraint(name).set_dual(value)
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
                self.ampl.set_option(name, value)

        return Options(self)

    var = property(_var)
    con = property(_con)
    obj = property(_obj)
    set = property(_set)
    param = property(_param)
    option = property(_option)

    def export_model(self, filename=""):
        """
        Create a .mod file with the model that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        return self.snapshot(filename, model=True, data=False, options=False)

    def export_data(self, filename=""):
        """
        Create a .dat file with the data that has been loaded.

        Args:
            filename: Path to the file (Relative to the current working
            directory or absolute).
        """
        return self.snapshot(filename, model=False, data=True, options=False)

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
        return self._impl.snapshot(filename, model, data, options)

    def write(self, filename, auxfiles=""):
        """
        Invoke write command with filename as argument and
        set auxfiles if non-empty.

        Args:
            filename: outuput filename.
            auxfiles: auxfiles to export.
        """
        try:
            self._impl.write(filename)
        except RuntimeError as e:
            message = str(e)
            if "presolve finds no feasible solution possible" in message:
                raise exceptions.InfeasibilityException(
                    message[message.find(":") + 1 :].lstrip()
                ) from None
            elif ":" in message:
                raise exceptions.PresolveException(
                    message[message.find(":") + 1 :].lstrip()
                ) from None
            else:
                raise

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

    def _start_recording(self, filename):
        """
        Start recording the session to a file for debug purposes.
        """
        filename = str(filename)
        self.set_option("_log_file_name", filename)
        self.set_option("_log_input_only", True)
        self.set_option("_log", True)

    def _stop_recording(self):
        """
        Stop recording the session.
        """
        self.set_option("_log", False)

    def _load_session(self, filename):
        """
        Load a recorded session.
        """
        filename = str(filename)
        try:
            self.eval(open(filename).read())
        except RuntimeError as exp:
            print(exp)

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
    writeTable = write_table
