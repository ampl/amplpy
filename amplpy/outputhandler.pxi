# -*- coding: utf-8 -*-

cdef class OutputHandler(object):
    """
    Interface to handle the outputs from the calls to any
    function that causes the underlying AMPL interpreter to display a message.
    If an application needs to
    implement customised output handling, it must implement this interface and
    then register an instance with the AMPL API using the
    :func:`~amplpy.AMPL.set_output_handler`
    method.

    Note that errors and warnings are not passed through this interface,
    see :class:`~amplpy.ErrorHandler` for more information.
    """

    def output(self, kind, msg):
        """
        This method is called when AMPL sends some output derived from
        executing a statement.

        Args:
           kind: kind of the output of the AMPL interpreter.

           msg: text of the output by the AMPL interpreter.
        """
        print(msg, end="", flush=True)

cdef void PyOutput(campl.AMPL_OUTPUTKIND kind, const char* msg, void* usrdata) except * with gil:
    PyOutputHandler = <OutputHandler>usrdata
    PyOutputHandler.output(kind, str(msg.decode('utf-8')))

class Kind(object):
    """
    Represents the type of the output coming from the interpreter.
    """

    """
    Output ``prompt2``, returned when incomplete statements are interpreted.
    """
    WAITING = campl.AMPL_OUTPUT_WAITING

    """
    Output ``break``, displayed when an operation is interrupted with SIGINT.
    """
    BREAK = campl.AMPL_OUTPUT_BREAK

    """
    Output ``cd``, returned by the ``cd`` function.
    """
    CD = campl.AMPL_OUTPUT_CD

    """
    Output ``display``, returned by the ``display`` function.
    """
    DISPLAY = campl.AMPL_OUTPUT_DISPLAY

    """
    Output ``exit``, returned as last message from AMPL before exiting the
    interpreter.
    """
    EXIT = campl.AMPL_OUTPUT_EXIT

    """
    Output ``expand``, returned by the ``expand`` function.
    """
    EXPAND = campl.AMPL_OUTPUT_EXPAND

    """
    Output ``load``, returned by the ``load`` function when loading a library.
    """
    LOAD = campl.AMPL_OUTPUT_LOAD

    """
    Output ``option``, returned by the ``option`` function when getting the
    value of an option.
    """
    OPTION = campl.AMPL_OUTPUT_OPTION

    """
    Output ``print``, returned by the ``print`` function when printing values
    from AMPL command line.
    """
    PRINT = campl.AMPL_OUTPUT_PRINT

    """
    Output ``prompt1``, normal AMPL prompt.
    """
    PROMPT = campl.AMPL_OUTPUT_PROMPT  # prompt1 and prompt3

    """
    Output ``solution``, returned when loading a solution with the command
    ``solution``, contains the solver message.
    """
    SOLUTION = campl.AMPL_OUTPUT_SOLUTION

    """
    Output ``solve``, returned by the ``solve`` function, contains the solver
    message.
    """
    SOLVE = campl.AMPL_OUTPUT_SOLVE

    """
    Output ``show``, returned by the ``show`` function.
    """
    SHOW = campl.AMPL_OUTPUT_SHOW

    """
    Output ``xref``, returned by the ``xref`` function.
    """
    XREF = campl.AMPL_OUTPUT_XREF

    """
    Output of the AMPL command ``shell``.
    """
    SHELL_OUTPUT = campl.AMPL_OUTPUT_SHELL_OUTPUT

    """
    Messages from the command ``shell``.
    """
    SHELL_MESSAGE = campl.AMPL_OUTPUT_SHELL_MESSAGE

    """
    Output ``misc``.
    """
    MISC = campl.AMPL_OUTPUT_MISC

    """
    Messages from the command ``write table``.
    """
    WRITE_TABLE = campl.AMPL_OUTPUT_WRITE_TABLE

    """
    Messages from the command ``read table``.
    """
    READ_TABLE = campl.AMPL_OUTPUT_READ_TABLE

    """
    Internal messages from the command ``read table``.
    """
    _READTABLE = campl.AMPL_OUTPUT_READTABLE

    """
    Internal messages from the command ``write table``.
    """
    _WRITETABLE = campl.AMPL_OUTPUT_WRITETABLE

    """
    Breakpoint hit.
    """
    BREAKPOINT = campl.AMPL_OUTPUT_BREAKPOINT

    """
    Output of a script ``call``.
    """
    CALL = campl.AMPL_OUTPUT_CALL

    """
    Output of a ``check`` operation.
    """
    CHECK = campl.AMPL_OUTPUT_CHECK

    """
    Output of a ``close`` command for output redirection.
    """
    CLOSE = campl.AMPL_OUTPUT_CLOSE

    """
    Output of a ``commands`` call into another file.
    """
    COMMANDS = campl.AMPL_OUTPUT_COMMANDS

    """
    Issued when ``continue`` is encountered.
    """
    CONTINUE = campl.AMPL_OUTPUT_CONTINUE

    """
    Output of a ``data`` command.
    """
    DATA = campl.AMPL_OUTPUT_DATA

    """
    Output of a ``delete`` command.
    """
    DELETECMD = campl.AMPL_OUTPUT_DELETECMD

    """
    Output of a ``drop`` command.
    """
    DROP = campl.AMPL_OUTPUT_DROP

    """
    Internal.
    """
    DROP_OR_RESTORE_ALL = campl.AMPL_OUTPUT_DROP_OR_RESTORE_ALL

    """
    Else block.
    """
    _ELSE = campl.AMPL_OUTPUT_ELSE

    """
    Internal.
    """
    ELSE_CHECK = campl.AMPL_OUTPUT_ELSE_CHECK

    """
    End of if block.
    """
    ENDIF = campl.AMPL_OUTPUT_ENDIF

    """
    Output of a ``environ`` command.
    """
    ENVIRON = campl.AMPL_OUTPUT_ENVIRON

    """
    Output of a ``fix`` command.
    """
    FIX = campl.AMPL_OUTPUT_FIX

    """
    Output of a ``for`` command.
    """
    FOR = campl.AMPL_OUTPUT_FOR

    """
    Output of an ``if`` command.
    """
    _IF = campl.AMPL_OUTPUT_IF

    """
    Output of a ``let`` command.
    """
    LET = campl.AMPL_OUTPUT_LET

    """
    End of loop.
    """
    LOOPEND = campl.AMPL_OUTPUT_LOOPEND

    """
    Output of an ``objective`` command.
    """
    OBJECTIVE = campl.AMPL_OUTPUT_OBJECTIVE

    """
    Occurs when resetting option values.
    """
    OPTION_RESET = campl.AMPL_OUTPUT_OPTION_RESET

    """
    Output of a ``printf`` command.
    """
    PRINTF = campl.AMPL_OUTPUT_PRINTF

    """
    Output of a ``problem`` command.
    """
    PROBLEM = campl.AMPL_OUTPUT_PROBLEM

    """
    Output of a ``purge`` command.
    """
    PURGE = campl.AMPL_OUTPUT_PURGE

    """
    Occurs when a right brace is encountered.
    """
    RBRACE = campl.AMPL_OUTPUT_RBRACE

    """
    Output of a ``read`` command.
    """
    READ = campl.AMPL_OUTPUT_READ

    """
    Output of a ``reload`` command.
    """
    RELOAD = campl.AMPL_OUTPUT_RELOAD

    """
    Output of a ``remove`` command.
    """
    REMOVE = campl.AMPL_OUTPUT_REMOVE

    """
    Beginning of a repeat loop.
    """
    REPEAT = campl.AMPL_OUTPUT_REPEAT

    """
    End of a repeat loop.
    """
    REPEAT_END = campl.AMPL_OUTPUT_REPEAT_END

    """
    Output of a ``reset`` command.
    """
    RESET = campl.AMPL_OUTPUT_RESET

    """
    Output of a ``restore`` command.
    """
    RESTORE = campl.AMPL_OUTPUT_RESTORE

    """
    Internal.
    """
    RUN_ARGS = campl.AMPL_OUTPUT_RUN_ARGS

    """
    Internal.
    """
    SEMICOLON = campl.AMPL_OUTPUT_SEMICOLON

    """
    Internal.
    """
    SSTEP = campl.AMPL_OUTPUT_SSTEP

    """
    Beginning of the ``then`` part of an if statement.
    """
    THEN = campl.AMPL_OUTPUT_THEN

    """
    Output of an ``unfix`` command.
    """
    UNFIX = campl.AMPL_OUTPUT_UNFIX

    """
    Output of an ``unload`` command.
    """
    UNLOAD = campl.AMPL_OUTPUT_UNLOAD

    """
    Output of an ``update`` command.
    """
    UPDATE = campl.AMPL_OUTPUT_UPDATE

    """
    Output of a ``write`` command.
    """
    WRITE = campl.AMPL_OUTPUT_WRITE
