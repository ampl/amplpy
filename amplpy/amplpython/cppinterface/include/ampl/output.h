#ifndef AMPL_OUTPUT_H_
#define AMPL_OUTPUT_H_

namespace ampl {

namespace output {
/**
 * Represents the type of the output coming from the interpreter
 */
enum Kind {
  /**
   * Output ``prompt2``, returned when incomplete statements are
   * interpreted
   */
  WAITING,

  /**
   * Output ``break``, displayed when an operation is interrupted with
   * SIGINT
   */
  BREAK,
  /**
   * Output ``cd``, returned by the ``cd`` function.
   */
  CD,
  /**
   * Output ``display``, returned by the ``display`` function.
   */
  DISPLAY,
  /**
   * Output ``exit``, returned as last message from %AMPL before
   * exiting the interpreter
   */
  EXIT,
  /**
   * Output ``expand``, returned by the ``expand`` function.
   */
  EXPAND,
  /**
   * Output ``load``, returned by the ``load`` function when loading a
   * library
   */
  LOAD,
  /**
   * Output ``option``, returned by the ``option`` function when
   * getting the value of an option
   */
  OPTION,
  /**
   * Output ``print``, returned by the ``print`` function when
   * printing values from %AMPL command line
   */
  PRINT,
  /**
   * Output ``prompt1``, normal %AMPL prompt
   */
  PROMPT,  // prompt1 and prompt3
           /**
            * Output ``solution``, returned when loading a solution with the
            * command ``solution``, contains the solver message
            */
  SOLUTION,
  /**
   * Output ``solve``, returned by the ``solve`` function, contains
   * the solver message
   */
  SOLVE,
  /**
   * Output ``show``, returned by the ``show`` function
   */
  SHOW,
  /**
   * Output ``xref``, returned by the ``xref`` function.
   */
  XREF,
  /**
   * Output of the %AMPL command ``shell``
   */
  SHELL_OUTPUT,
  /**
   * Messages from the command ``shell``
   */
  SHELL_MESSAGE,
  /**
   * Output ``misc``
   */
  MISC,
  /**
   * Messages from the command ``write table``
   */
  WRITE_TABLE,
  /**
   * Messages from the command ``read table``
   */
  READ_TABLE,
  /**
   * Internal messages from the command ``read table``
   */
  _READTABLE,
  /**
   * Internal messages from the command ``write table``
   */
  _WRITETABLE,
  /**
   * Breakpoint hit
   */
  BREAKPOINT,
  /**
   * Output of a script ``call``
   */
  CALL,
  /**
   * Output of a ``check`` operation
   */
  CHECK,
  /**
   * Output of a ``close`` command for output redirection
   */
  CLOSE,
  /**
   * Output of a ``commands`` call into another file
   */
  COMMANDS,
  /**
   * Issued when ``continue`` is encountered
   */
  CONTINUE,
  /**
   * Output of a ``data`` command
   */
  DATA,
  /**
   * Output of a ``delete`` command
   */
  DELETECMD,
  /**
   * Output of a ``drop`` command
   */
  DROP,
  /**
   * Internal
   */
  DROP_OR_RESTORE_ALL,
  /**
   * Else block
   */
  ELSE,
  /**
   * Internal
   */
  ELSE_CHECK,
  /**
   * End of if block
   */
  ENDIF,
  /**
   * Output of a ``environ`` command
   */
  ENVIRON,
  /**
   * Output of a ``fix`` command
   */
  FIX,
  /**
   * Output of a ``for`` command
   */
  FOR,
  /**
   * Output of an ``if`` command
   */
  IF,
  /**
   * Output of a ``let`` command
   */
  LET,
  /**
   * End of loop
   */
  LOOPEND,
  /**
   * Output of an ``objective`` command
   */
  OBJECTIVE,
  /**
   * Occurs when resetting option values
   */
  OPTION_RESET,
  /**
   * Output of a ``printf`` command
   */
  PRINTF,
  /**
   * Output of a ``problem`` command
   */
  PROBLEM,
  /**
   * Output of a ``purge`` command
   */
  PURGE,
  /**
   * Occurs when a right brace is encountered
   */
  RBRACE,
  /**
   * Output of a ``read`` command
   */
  READ,
  /**
   * Output of a ``reload`` command
   */
  RELOAD,
  /**
   * Output of a ``remove`` command
   */
  REMOVE,
  /**
   * Beginning of a repeat loop
   */
  REPEAT,
  /**
   * End of a repeat loop
   */
  REPEAT_END,
  /**
   * Output of a ``reset`` command
   */
  RESET,
  /**
   * Output of a ``restore`` command
   */
  RESTORE,
  /**
   * Internal
   */
  RUN_ARGS,
  /**
   * Internal
   */
  SEMICOLON,
  /**
   * Internal
   */
  SSTEP,
  /**
   * Beginning of the ``then`` part of an if statement
   */
  THEN,
  /**
   * Output of an ``unfix`` command
   */
  UNFIX,
  /**
   * Output of an ``unload`` command
   */
  UNLOAD,
  /**
   * Output of an ``update`` command
   */
  UPDATE,
  /**
   * Output of a ``write`` command
   */
  WRITE
};
}  // namespace output

/**
 * Implement this interface to handle the outputs from the calls to any
 * function that causes the underlying %AMPL interpreter to display a message.
 * <p>
 * Note that errors and warnings are not passed through this interface,
 * see ampl::ErrorHandler for more information.
 */
class OutputHandler {
 public:
  virtual ~OutputHandler() {}
  /**
   * This method is called when %AMPL sends some output derived from executing a
   * statement
   * @param kind kind of the output of the %AMPL interpreter
   * @param msg text of the output by the %AMPL interpreter
   */
  virtual void output(output::Kind kind, const char* msg) = 0;
};

}  // namespace ampl

#endif  // AMPL_OUTPUT_H_
