# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
from builtins import object

# from past.builtins import basestring

from . import amplpython


class OutputHandler(amplpython.OutputHandler):
    """
    Interface to handle the outputs from the calls to any
    function that causes the underlying AMPL interpreter to display a message.
    If an application needs to
    implement customised output handling, it must implement this interface and
    then register an instance with the AMPL API using the
    :func:`~amplpy.AMPL.set_output_handler` / :func:`~amplpy.AMPL.setOutputHandler`
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
        print(msg, end="")


class Kind(object):
    """
    Represents the type of the output coming from the interpreter.
    """

    WAITING = amplpython.WAITING
    """
    Output ``prompt2``, returned when incomplete statements are interpreted.
    """

    BREAK = amplpython.BREAK
    """
    Output ``break``, displayed when an operation is interrupted with SIGINT.
    """

    CD = amplpython.CD
    """
    Output ``cd``, returned by the ``cd`` function.
    """

    DISPLAY = amplpython.DISPLAY
    """
    Output ``display``, returned by the ``display`` function.
    """

    EXIT = amplpython.EXIT
    """
    Output ``exit``, returned as last message from AMPL before exiting the
    interpreter.
    """

    EXPAND = amplpython.EXPAND
    """
    Output ``expand``, returned by the ``expand`` function.

    """

    LOAD = amplpython.LOAD
    """
    Output ``load``, returned by the ``load`` function when loading a library.
    """

    OPTION = amplpython.OPTION
    """
    Output ``option``, returned by the ``option`` function when getting the
    value of an option.
    """

    PRINT = amplpython.PRINT
    """
    Output ``print``, returned by the ``print`` function when printing values
    from AMPL command line.
    """

    PROMPT = amplpython.PROMPT  # prompt1 and prompt3
    """
    Output ``prompt1``, normal AMPL prompt.
    """

    SOLUTION = amplpython.SOLUTION
    """
    Output ``solution``, returned when loading a solution with the command
    ``solution``, contains the solver message.
    """

    SOLVE = amplpython.SOLVE
    """
    Output ``solve``, returned by the ``solve`` function, contains the solver
    message.
    """

    SHOW = amplpython.SHOW
    """
    Output ``show``, returned by the ``show`` function.
    """

    XREF = amplpython.XREF
    """
    Output ``xref``, returned by the ``xref`` function.
    """

    SHELL_OUTPUT = amplpython.SHELL_OUTPUT
    """
    Output of the AMPL command ``shell``.
    """

    SHELL_MESSAGE = amplpython.SHELL_MESSAGE
    """
    Messages from the command ``shell``.
    """

    MISC = amplpython.MISC
    """
    Output ``misc``.
    """

    WRITE_TABLE = amplpython.WRITE_TABLE
    """
    Messages from the command ``write table``.
    """

    READ_TABLE = amplpython.READ_TABLE
    """
    Messages from the command ``read table``.
    """

    _READTABLE = amplpython._READTABLE
    """
    Internal messages from the command ``read table``.
    """

    _WRITETABLE = amplpython._WRITETABLE
    """
    Internal messages from the command ``write table``.
    """

    BREAKPOINT = amplpython.BREAKPOINT
    """
    Breakpoint hit.
    """

    CALL = amplpython.CALL
    """
    Output of a script ``call``.

    """

    CHECK = amplpython.CHECK
    """
    Output of a ``check`` operation.
    """

    CLOSE = amplpython.CLOSE
    """
    Output of a ``close`` command for output redirection.
    """

    COMMANDS = amplpython.COMMANDS
    """
    Output of a ``commands`` call into another file.
    """

    CONTINUE = amplpython.CONTINUE
    """
    Issued when ``continue`` is encountered.
    """

    DATA = amplpython.DATA
    """
    Output of a ``data`` command.
    """

    DELETECMD = amplpython.DELETECMD
    """
    Output of a ``delete`` command.
    """

    DROP = amplpython.DROP
    """
    Output of a ``drop`` command.
    """

    DROP_OR_RESTORE_ALL = amplpython.DROP_OR_RESTORE_ALL
    """
    Internal.
    """

    ELSE = amplpython.ELSE
    """
    Else block.
    """

    ELSE_CHECK = amplpython.ELSE_CHECK
    """
    Internal.
    """

    ENDIF = amplpython.ENDIF
    """
    End of if block.
    """

    ENVIRON = amplpython.ENVIRON
    """
    Output of a ``environ`` command.
    """

    FIX = amplpython.FIX
    """
    Output of a ``fix`` command.
    """

    FOR = amplpython.FOR
    """
    Output of a ``for`` command.
    """

    IF = amplpython.IF
    """
    Output of an ``if`` command.
    """

    LET = amplpython.LET
    """
    Output of a ``let`` command.
    """

    LOOPEND = amplpython.LOOPEND
    """
    End of loop.
    """

    OBJECTIVE = amplpython.OBJECTIVE
    """
    Output of an ``objective`` command.
    """

    OPTION_RESET = amplpython.OPTION_RESET
    """
    Occurs when resetting option values.
    """

    PRINTF = amplpython.PRINTF
    """
    Output of a ``printf`` command.
    """

    PROBLEM = amplpython.PROBLEM
    """
    Output of a ``problem`` command.
    """

    PURGE = amplpython.PURGE
    """
    Output of a ``purge`` command.
    """

    RBRACE = amplpython.RBRACE
    """
    Occurs when a right brace is encountered.
    """

    READ = amplpython.READ
    """
    Output of a ``read`` command.
    """

    RELOAD = amplpython.RELOAD
    """
    Output of a ``reload`` command.
    """

    REMOVE = amplpython.REMOVE
    """
    Output of a ``remove`` command.
    """

    REPEAT = amplpython.REPEAT
    """
    Beginning of a repeat loop.
    """

    REPEAT_END = amplpython.REPEAT_END
    """
    End of a repeat loop.
    """

    RESET = amplpython.RESET
    """
    Output of a ``reset`` command.
    """

    RESTORE = amplpython.RESTORE
    """
    Output of a ``restore`` command.
    """

    RUN_ARGS = amplpython.RUN_ARGS
    """
    Internal.
    """

    SEMICOLON = amplpython.SEMICOLON
    """
    Internal.
    """

    SSTEP = amplpython.SSTEP
    """
    Internal.
    """

    THEN = amplpython.THEN
    """
    Beginning of the ``then`` part of an if statement.
    """

    UNFIX = amplpython.UNFIX
    """
    Output of an ``unfix`` command.
    """

    UNLOAD = amplpython.UNLOAD
    """
    Output of an ``unload`` command.
    """

    UPDATE = amplpython.UPDATE
    """
    Output of an ``update`` command.
    """

    WRITE = amplpython.WRITE
    """
    Output of a ``write`` command.
    """
