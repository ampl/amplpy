# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from threading import Thread, Lock
from .errorhandler import ErrorHandler
from .outputhandler import OutputHandler
from .objective import Objective
from .variable import Variable
from .constraint import Constraint
from .set import Set
from .parameter import Parameter
from .dataframe import DataFrame
from .iterators import EntityMap
from .exceptions import AMPLException
from .entity import Entity
from .utils import Utils, lock_call
from . import amplpython


class AMPL(object):
    """An AMPL translator.

    An object of this class can be used to do the following tasks:

    - Run AMPL code. See :func:`~amplpy.AMPL.eval` and
      :func:`~amplpy.AMPL.evalAsync`.
    - Read models and data from files. See :func:`~amplpy.AMPL.read`,
      :func:`~amplpy.AMPL.readData`, :func:`~amplpy.AMPL.readAsync`, and
      :func:`~amplpy.AMPL.readDataAsync`.
    - Solve optimization problems constructed from model and data (see
      :func:`~amplpy.AMPL.solve` and :func:`~amplpy.AMPL.solveAsync`).
    - Access single Elements of an optimization problem. See
      :func:`~amplpy.AMPL.getVariable`, :func:`~amplpy.AMPL.getConstraint`,
      :func:`~amplpy.AMPL.getObjective`, :func:`~amplpy.AMPL.getSet`,
      and :func:`~amplpy.AMPL.getParameter`.
    - Access lists of available entities of an optimization problem. See
      :func:`~amplpy.AMPL.getVariables`, :func:`~amplpy.AMPL.getConstraints`,
      :func:`~amplpy.AMPL.getObjectives`, :func:`~amplpy.AMPL.getSets`,
      and :func:`~amplpy.AMPL.getParameters`.

    Error handling is two-faced:

    - Errors coming from the underlying AMPL translator (e.g. syntax errors and
      warnings obtained calling the eval method) are handled by
      the :class:`~amplpy.ErrorHandler` which can be set and get via
      :func:`~amplpy.AMPL.getErrorHandler` and
      :func:`~amplpy.AMPL.setErrorHandler`.
    - Generic errors coming from misusing the API, which are detected in
      Python, are thrown as exceptions.

    The default implementation of the error handler throws exceptions on errors
    and prints to console on warnings.

    The output of every user interaction with the underlying translator is
    handled implementing the abstract class :class:`~amplpy.OutputHandler`.
    The (only) method is called at each block of output from the translator.
    The current output handler can be accessed and set via
    :func:`~amplpy.AMPL.getOutputHandler` and
    :func:`~amplpy.AMPL.setOutputHandler`.
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
        if environment is None:
            self._impl = amplpython.AMPL()
        else:
            self._impl = amplpython.AMPL(environment._impl)
        self._errorhandler = None
        self._outputhandler = None
        self._lock = Lock()

    def __del__(self):
        """
        Default destructor:
        releases all the resources related to the AMPL instance (most notably
        kills the underlying  interpreter).
        """
        self.close()

    def getData(self, *statements):
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
            RuntimeError: if the AMPL visualization command does not succeed
            for one of the reasons listed above.

        Returns:
            DataFrame capturing the output of the display
            command in tabular form.
        """
        # FIXME: only works for the first statement.
        return lock_call(
            lambda: DataFrame._fromDataFrameRef(
                self._impl.getData(list(statements), len(statements))
            ),
            self._lock
        )

    def getEntity(self, name):
        """
        Get entity corresponding to the specified name (looks for it in all
        types of entities).

        Args:
            name: Name of the entity.

        Raises:
            TypeError: if the specified entity does not exist.

        Returns:
            The AMPL entity with the specified name.
        """
        return lock_call(
            lambda: Entity(self._impl.getEntity(name)),
            self._lock
        )

    def getVariable(self, name):
        """
        Get the variable with the corresponding name.

        Args:
            name: Name of the variable to be found.

        Raises:
            TypeError: if the specified variable does not exist.
        """
        return lock_call(
            lambda: Variable(self._impl.getVariable(name)),
            self._lock
        )

    def getConstraint(self, name):
        """
        Get the constraint with the corresponding name.

        Args:
            name: Name of the constraint to be found.

        Raises:
            TypeError: if the specified constraint does not exist.
        """
        return lock_call(
            lambda: Constraint(self._impl.getConstraint(name)),
            self._lock
        )

    def getObjective(self, name):
        """
         Get the objective with the corresponding name.

         Args:
            name: Name of the objective to be found.

        Raises:
            TypeError: if the specified objective does not exist.
        """
        return lock_call(
            lambda: Objective(self._impl.getObjective(name)),
            self._lock
        )

    def getSet(self, name):
        """
        Get the set with the corresponding name.

        Args:
            name: Name of the set to be found.

        Raises:
            TypeError: if the specified set does not exist.
        """
        return lock_call(
            lambda: Set(self._impl.getSet(name)),
            self._lock
        )

    def getParameter(self, name):
        """
        Get the parameter with the corresponding name.

        Args:
            name: Name of the parameter to be found.

        Raises:
            TypeError: if the specified parameter does not exist.
        """
        return lock_call(
            lambda: Parameter(self._impl.getParameter(name)),
            self._lock
        )

    def eval(self, amplstatements):
        """
        Parses AMPL code and evaluates it as a possibly empty sequence of AMPL
        declarations and statements.

        As a side effect, it invalidates all entities (as the passed statements
        can contain any arbitrary command); the lists of entities will be
        re-populated lazily (at first access)

        The output of interpreting the statements is passed to the current
        OutputHandler (see getOutputHandler and
        setOutputHandler).

        By default, errors are reported as exceptions and warnings are printed
        on stdout. This behavior can be changed reassigning an ErrorHandler
        using setErrorHandler.

        Args:
          amplstatements: A collection of AMPL statements and declarations to
          be passed to the interpreter.

        Raises:
          RuntimeError: if the input is not a complete AMPL statement (e.g.
          if it does not end with semicolon) or if the underlying
          interpreter is not running.
        """
        lock_call(
            lambda: self._impl.eval(amplstatements),
            self._lock
        )

    def reset(self):
        """
        Clears all entities in the underlying AMPL interpreter, clears all maps
        and invalidates all entities.
        """
        # self._impl.reset()  # FIXME: causes Segmentation fault
        self.eval('reset;')

    def close(self):
        """
        Stops the underlying engine, and release all any further attempt to
        execute optimization commands without restarting it will throw an
        exception.
        """
        self._impl.close()

    def isRunning(self):
        """
        Returns true if the underlying engine is running.
        """
        return lock_call(
            lambda: self._impl.isRunning(),
            self._lock
        )

    def isBusy(self):
        """
        Returns true if the underlying engine is doing an async operation.
        """
        # return self._impl.isBusy()
        if self._lock.acquire(False):
            self._lock.release()
            return False
        else:
            return True

    def solve(self):
        """
        Solve the current model.

        Raises:
            RuntimeError: if the underlying interpreter is not running.
        """
        return lock_call(
            lambda: self._impl.solve(),
            self._lock
        )

    def readAsync(self, fileName, callback):
        """
        Interprets the specified file asynchronously, interpreting it as a
        model or a script file. As a side effect, it invalidates all entities
        (as the passed file can contain any arbitrary command); the lists of
        entities will be re-populated lazily (at first access).

        Args:
            fileName: Path to the file (Relative to the current working
            directory or absolute).

            callback: Callback to be executed when the file has been
            interpreted.
        """
        def async():
            self._lock.acquire()
            try:
                self._impl.read(fileName)
            except Exception:
                self._lock.release()
                raise
            else:
                self._lock.release()
                callback.run()
        Thread(target=async).start()

    def readDataAsync(self, fileName, callback):
        """
        Interprets the specified data file asynchronously. When interpreting is
        over, the specified callback is called. The file is interpreted as
        data. As a side effect, it invalidates all entities (as the passed file
        can contain any arbitrary command); the lists of entities will be
        re-populated lazily (at first access)

        Args:
            fileName: Full path to the file.

            callback: Callback to be executed when the file has been
            interpreted.
        """
        def async():
            self._lock.acquire()
            try:
                self._impl.readData(fileName)
            except Exception:
                self._lock.release()
                raise
            else:
                self._lock.release()
                callback.run()
        Thread(target=async).start()

    def evalAsync(self, amplstatements, callback):
        """
        Interpret the given AMPL statement asynchronously.

        Args:
          amplstatements: A collection of AMPL statements and declarations to
          be passed to the interpreter.

          callback: Callback to be executed when the statement has been
          interpreted.

        Raises:
          RuntimeError: if the input is not a complete AMPL statement (e.g.
          if it does not end with semicolon) or if the underlying
          interpreter is not running.
        """
        def async():
            self._lock.acquire()
            try:
                self._impl.eval(amplstatements)
            except Exception:
                self._lock.release()
                raise
            else:
                self._lock.release()
                callback.run()
        Thread(target=async).start()

    def solveAsync(self, callback):
        """
        Solve the current model asynchronously.

        Args:
          callback: Callback to be executed when the solver is done.
        """
        def async():
            self._lock.acquire()
            try:
                self._impl.solve()
            except Exception:
                self._lock.release()
                raise
            else:
                self._lock.release()
                callback.run()
        Thread(target=async).start()

    def wait(self):
        """
        Wait for the current async operation to finish.
        """
        self._lock.acquire()
        self._lock.release()

    def interrupt(self):
        """
        Interrupt an underlying asynchronous operation (execution of AMPL code
        by the AMPL interpreter). An asynchronous operation can be started via
        evalAsync(), solveAsync(), readAsync() and readDataAsync().
        Does nothing if the engine and the solver are idle.
        """
        self._impl.interrupt()

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
            return lock_call(
                lambda: self._impl.cd(),
                self._lock
            )
        else:
            return lock_call(
                lambda: self._impl.cd(path),
                self._lock
            )

    def setOption(self, name, value):
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
            lock_call(
                lambda: self._impl.setBoolOption(name, value),
                self._lock
            )
        elif isinstance(value, int):
            lock_call(
                lambda: self._impl.setIntOption(name, value),
                self._lock
            )
        elif isinstance(value, float):
            lock_call(
                lambda: self._impl.setDblOption(name, value),
                self._lock
            )
        elif isinstance(value, basestring):
            lock_call(
                lambda: self._impl.setOption(name, value),
                self._lock
            )
        else:
            raise TypeError

    def getOption(self, name):
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
            value = lock_call(
                lambda: self._impl.getOption(name).value(),
                self._lock
            )
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

    def read(self, fileName):
        """
        Interprets the specified file (script or model or mixed) As a side
        effect, it invalidates all entities (as the passed file can contain any
        arbitrary command); the lists of entities will be re-populated lazily
        (at first access).

        Args:
            fileName: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        lock_call(
            lambda: self._impl.read(fileName),
            self._lock
        )

    def readData(self, fileName):
        """
        Interprets the specified file as an AMPL data file. As a side effect,
        it invalidates all entities (as the passed file can contain any
        arbitrary command); the lists of entities will be re-populated lazily
        (at first access). After reading the file, the interpreter is put back
        to "model" mode.

        Args:
            fileName: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        lock_call(
            lambda: self._impl.readData(fileName),
            self._lock
        )

    def getValue(self, scalarExpression):
        """
        Get a scalar value from the underlying AMPL interpreter, as a double or
        a string.

        Args:
            scalarExpression: An AMPL expression which evaluates to a scalar
            value.

        Returns:
            The value of the expression.
        """
        return lock_call(
            lambda: Utils.castVariant(self._impl.getValue(scalarExpression)),
            self._lock
        )

    def setData(self, dataFrame, setName=None):
        """
        Assign the data in the dataframe to the AMPL entities with the names
        corresponding to the column names.

        Args:
            dataFrame: The dataframe containing the data to be assigned.

            setName: The name of the set to which the indices values of the
            DataFrame are to be assigned.

        Raises:
            AMPLException: if the data assignment procedure was not successful.
        """
        if setName is None:
            lock_call(
                lambda: self._impl.setData(dataFrame._impl),
                self._lock
            )
        else:
            lock_call(
                lambda: self._impl.setData(dataFrame._impl, setName),
                self._lock
            )

    def readTable(self, tableName):
        """
        Read the table corresponding to the specified name, equivalent to the
        AMPL statement:

        .. code-block:: ampl

            read table tableName;

        Args:
            tableName: Name of the table to be read.
        """
        lock_call(
            lambda: self._impl.readTable(tableName),
            self._lock
        )

    def writeTable(self, tableName):
        """
        Write the table corresponding to the specified name, equivalent to the
        AMPL statement

        .. code-block:: ampl

            write table tableName;

        Args:
            tableName: Name of the table to be written.
        """
        lock_call(
            lambda: self._impl.writeTable(tableName),
            self._lock
        )

    def display(self, *amplExpressions):
        """
        Writes on the current OutputHandler the outcome of the AMPL statement.

        .. code-block:: ampl

            display e1, e2, .., en;

        where e1, ..., en are the strings passed to the procedure.

        Args:
            amplExpressions: Expressions to be evaluated.
        """
        exprs = list(map(str, amplExpressions))
        lock_call(
            lambda: self._impl.displayLst(exprs, len(exprs)),
            self._lock
        )

    def setOutputHandler(self, outputhandler):
        """
        Sets a new output handler.

        Args:
            outputhandler: The function handling the AMPL output derived from
            interpreting user commands.
        """
        class OutputHandlerInternal(OutputHandler):
            def output(self, kind, msg):
                outputhandler.output(kind, msg)

        self._outputhandler = outputhandler
        self._outputhandler_internal = OutputHandlerInternal()
        lock_call(
            lambda: self._impl.setOutputHandler(
                self._outputhandler_internal
            ),
            self._lock
        )

    def setErrorHandler(self, errorhandler):
        """
        Sets a new error handler.

        Args:
            errorhandler: The object handling AMPL errors and warnings.
        """
        class InternalErrorHandler(ErrorHandler):
            def error(self, exception):
                if isinstance(exception, amplpython.AMPLException):
                    exception = AMPLException(exception)
                errorhandler.error(exception)

            def warning(self, exception):
                if isinstance(exception, amplpython.AMPLException):
                    exception = AMPLException(exception)
                errorhandler.warning(exception)

        self._errorhandler = errorhandler
        self._errorhandler_internal = InternalErrorHandler()
        lock_call(
            lambda: self._impl.setErrorHandler(self._errorhandler_internal),
            self._lock
        )

    def getOutputHandler(self):
        """
        Get the current output handler.

        Returns:
            The current output handler.
        """
        return self._outputhandler

    def getErrorHandler(self):
        """
        Get the current error handler.

        Returns:
            The current error handler.
        """
        return self._errorhandler

    def getVariables(self):
        """
        Get all the variables declared.
        """
        variables = lock_call(
            lambda: self._impl.getVariables(),
            self._lock
        )
        return EntityMap(variables, Variable)

    def getConstraints(self):
        """
        Get all the constraints declared.
        """
        constraints = lock_call(
            lambda: self._impl.getConstraints(),
            self._lock
        )
        return EntityMap(constraints, Constraint)

    def getObjectives(self):
        """
        Get all the objectives declared.
        """
        objectives = lock_call(
            lambda: self._impl.getObjectives(),
            self._lock
        )
        return EntityMap(objectives, Objective)

    def getSets(self):
        """
        Get all the sets declared.
        """
        sets = lock_call(
            lambda: self._impl.getSets(),
            self._lock
        )
        return EntityMap(sets, Set)

    def getParameters(self):
        """
        Get all the parameters declared.
        """
        parameters = lock_call(
            lambda: self._impl.getParameters(),
            self._lock
        )
        return EntityMap(parameters, Parameter)
