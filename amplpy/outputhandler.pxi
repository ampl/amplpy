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
    PyOutputHandler.output(kind, msg.decode('utf-8'))

class Kind(object):
    """
    Represents the type of the output coming from the interpreter.
    """

    WAITING = campl.AMPL_OUTPUT_WAITING
    """
    Output ``prompt2``, returned when incomplete statements are interpreted.
    """

    BREAK = campl.AMPL_OUTPUT_BREAK
    """
    Output ``break``, displayed when an operation is interrupted with SIGINT.
    """

    CD = campl.AMPL_OUTPUT_CD
    """
    Output ``cd``, returned by the ``cd`` function.
    """

    DISPLAY = campl.AMPL_OUTPUT_DISPLAY
    """
    Output ``display``, returned by the ``display`` function.
    """

    EXIT = campl.AMPL_OUTPUT_EXIT
    """
    Output ``exit``, returned as last message from AMPL before exiting the
    interpreter.
    """

    EXPAND = campl.AMPL_OUTPUT_EXPAND
    """
    Output ``expand``, returned by the ``expand`` function.
    """

    LOAD = campl.AMPL_OUTPUT_LOAD
    """
    Output ``load``, returned by the ``load`` function when loading a library.
    """

    OPTION = campl.AMPL_OUTPUT_OPTION
    """
    Output ``option``, returned by the ``option`` function when getting the
    value of an option.
    """

    PRINT = campl.AMPL_OUTPUT_PRINT
    """
    Output ``print``, returned by the ``print`` function when printing values
    from AMPL command line.
    """

    PROMPT = campl.AMPL_OUTPUT_PROMPT  # prompt1 and prompt3
    """
    Output ``prompt1``, normal AMPL prompt.
    """

    SOLUTION = campl.AMPL_OUTPUT_SOLUTION
    """
    Output ``solution``, returned when loading a solution with the command
    ``solution``, contains the solver message.
    """

    SOLVE = campl.AMPL_OUTPUT_SOLVE
    """
    Output ``solve``, returned by the ``solve`` function, contains the solver
    message.
    """

    SHOW = campl.AMPL_OUTPUT_SHOW
    """
    Output ``show``, returned by the ``show`` function.
    """

    XREF = campl.AMPL_OUTPUT_XREF
    """
    Output ``xref``, returned by the ``xref`` function.
    """

    SHELL_OUTPUT = campl.AMPL_OUTPUT_SHELL_OUTPUT
    """
    Output of the AMPL command ``shell``.
    """

    SHELL_MESSAGE = campl.AMPL_OUTPUT_SHELL_MESSAGE
    """
    Messages from the command ``shell``.
    """

    MISC = campl.AMPL_OUTPUT_MISC
    """
    Output ``misc``.
    """

    WRITE_TABLE = campl.AMPL_OUTPUT_WRITE_TABLE
    """
    Messages from the command ``write table``.
    """

    READ_TABLE = campl.AMPL_OUTPUT_READ_TABLE
    """
    Messages from the command ``read table``.
    """

    _READTABLE = campl.AMPL_OUTPUT_READTABLE
    """
    Internal messages from the command ``read table``.
    """

    _WRITETABLE = campl.AMPL_OUTPUT_WRITETABLE
    """
    Internal messages from the command ``write table``.
    """

    BREAKPOINT = campl.AMPL_OUTPUT_BREAKPOINT
    """
    Breakpoint hit.
    """

    CALL = campl.AMPL_OUTPUT_CALL
    """
    Output of a script ``call``.
    """

    CHECK = campl.AMPL_OUTPUT_CHECK
    """
    Output of a ``check`` operation.
    """

    CLOSE = campl.AMPL_OUTPUT_CLOSE
    """
    Output of a ``close`` command for output redirection.
    """

    COMMANDS = campl.AMPL_OUTPUT_COMMANDS
    """
    Output of a ``commands`` call into another file.
    """

    CONTINUE = campl.AMPL_OUTPUT_CONTINUE
    """
    Issued when ``continue`` is encountered.
    """

    DATA = campl.AMPL_OUTPUT_DATA
    """
    Output of a ``data`` command.
    """

    DELETECMD = campl.AMPL_OUTPUT_DELETECMD
    """
    Output of a ``delete`` command.
    """

    DROP = campl.AMPL_OUTPUT_DROP
    """
    Output of a ``drop`` command.
    """

    DROP_OR_RESTORE_ALL = campl.AMPL_OUTPUT_DROP_OR_RESTORE_ALL
    """
    Internal.
    """

    _ELSE = campl.AMPL_OUTPUT_ELSE
    """
    Else block.
    """

    ELSE_CHECK = campl.AMPL_OUTPUT_ELSE_CHECK
    """
    Internal.
    """

    ENDIF = campl.AMPL_OUTPUT_ENDIF
    """
    End of if block.
    """

    ENVIRON = campl.AMPL_OUTPUT_ENVIRON
    """
    Output of a ``environ`` command.
    """

    FIX = campl.AMPL_OUTPUT_FIX
    """
    Output of a ``fix`` command.
    """

    FOR = campl.AMPL_OUTPUT_FOR
    """
    Output of a ``for`` command.
    """

    _IF = campl.AMPL_OUTPUT_IF
    """
    Output of an ``if`` command.
    """

    LET = campl.AMPL_OUTPUT_LET
    """
    Output of a ``let`` command.
    """

    LOOPEND = campl.AMPL_OUTPUT_LOOPEND
    """
    End of loop.
    """

    OBJECTIVE = campl.AMPL_OUTPUT_OBJECTIVE
    """
    Output of an ``objective`` command.
    """

    OPTION_RESET = campl.AMPL_OUTPUT_OPTION_RESET
    """
    Occurs when resetting option values.
    """

    PRINTF = campl.AMPL_OUTPUT_PRINTF
    """
    Output of a ``printf`` command.
    """

    PROBLEM = campl.AMPL_OUTPUT_PROBLEM
    """
    Output of a ``problem`` command.
    """

    PURGE = campl.AMPL_OUTPUT_PURGE
    """
    Output of a ``purge`` command.
    """

    RBRACE = campl.AMPL_OUTPUT_RBRACE
    """
    Occurs when a right brace is encountered.
    """

    READ = campl.AMPL_OUTPUT_READ
    """
    Output of a ``read`` command.
    """

    RELOAD = campl.AMPL_OUTPUT_RELOAD
    """
    Output of a ``reload`` command.
    """

    REMOVE = campl.AMPL_OUTPUT_REMOVE
    """
    Output of a ``remove`` command.
    """

    REPEAT = campl.AMPL_OUTPUT_REPEAT
    """
    Beginning of a repeat loop.
    """

    REPEAT_END = campl.AMPL_OUTPUT_REPEAT_END
    """
    End of a repeat loop.
    """

    RESET = campl.AMPL_OUTPUT_RESET
    """
    Output of a ``reset`` command.
    """

    RESTORE = campl.AMPL_OUTPUT_RESTORE
    """
    Output of a ``restore`` command.
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
    Internal.
    """

    THEN = campl.AMPL_OUTPUT_THEN
    """
    Beginning of the ``then`` part of an if statement.
    """

    UNFIX = campl.AMPL_OUTPUT_UNFIX
    """
    Output of an ``unfix`` command.
    """

    UNLOAD = campl.AMPL_OUTPUT_UNLOAD
    """
    Output of an ``unload`` command.
    """

    UPDATE = campl.AMPL_OUTPUT_UPDATE
    """
    Output of an ``update`` command.
    """

    WRITE = campl.AMPL_OUTPUT_WRITE
    """
    Output of a ``write`` command.
    """
