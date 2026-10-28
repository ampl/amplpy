#ifndef AMPL_OUTPUT_C_H
#define AMPL_OUTPUT_C_H

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * \defgroup AMPL_OUTPUTKIND AMPL Outputkinds functions
 * @{
 *
 */

/**
 * Represents the type of the output coming from the interpreter
 */
typedef enum {
  /**
   * Output ``prompt2``, returned when incomplete statements are
   * interpreted
   */
  AMPL_OUTPUT_WAITING,

  /**
   * Output ``break``, displayed when an operation is interrupted with
   * SIGINT
   */
  AMPL_OUTPUT_BREAK,
  /**
   * Output ``cd``, returned by the ``cd`` function.
   */
  AMPL_OUTPUT_CD,
  /**
   * Output ``display``, returned by the ``display`` function.
   */
  AMPL_OUTPUT_DISPLAY,
  /**
   * Output ``exit``, returned as last message from %AMPL before
   * exiting the interpreter
   */
  AMPL_OUTPUT_EXIT,
  /**
   * Output ``expand``, returned by the ``expand`` function.
   */
  AMPL_OUTPUT_EXPAND,
  /**
   * Output ``load``, returned by the ``load`` function when loading a
   * library
   */
  AMPL_OUTPUT_LOAD,
  /**
   * Output ``option``, returned by the ``option`` function when
   * getting the value of an option
   */
  AMPL_OUTPUT_OPTION,
  /**
   * Output ``print``, returned by the ``print`` function when
   * printing values from %AMPL command line
   */
  AMPL_OUTPUT_PRINT,
  /**
   * Output ``prompt1``, normal %AMPL prompt
   */
  AMPL_OUTPUT_PROMPT,  // prompt1 and prompt3
           /**
            * Output ``solution``, returned when loading a solution with the
            * command ``solution``, contains the solver message
            */
  AMPL_OUTPUT_SOLUTION,
  /**
   * Output ``solve``, returned by the ``solve`` function, contains
   * the solver message
   */
  AMPL_OUTPUT_SOLVE,
  /**
   * Output ``show``, returned by the ``show`` function
   */
  AMPL_OUTPUT_SHOW,
  /**
   * Output ``xref``, returned by the ``xref`` function.
   */
  AMPL_OUTPUT_XREF,
  /**
   * Output of the %AMPL command ``shell``
   */
  AMPL_OUTPUT_SHELL_OUTPUT,
  /**
   * Messages from the command ``shell``
   */
  AMPL_OUTPUT_SHELL_MESSAGE,
  /**
   * Output ``misc``
   */
  AMPL_OUTPUT_MISC,
  /**
   * Messages from the command ``write table``
   */
  AMPL_OUTPUT_WRITE_TABLE,
  /**
   * Messages from the command ``read table``
   */
  AMPL_OUTPUT_READ_TABLE,
  /**
   * Internal messages from the command ``read table``
   */
  AMPL_OUTPUT_READTABLE,
  /**
   * Internal messages from the command ``write table``
   */
  AMPL_OUTPUT_WRITETABLE,
  /**
   * Breakpoint hit
   */
  AMPL_OUTPUT_BREAKPOINT,
  /**
   * Output of a script ``call``
   */
  AMPL_OUTPUT_CALL,
  /**
   * Output of a ``check`` operation
   */
  AMPL_OUTPUT_CHECK,
  /**
   * Output of a ``close`` command for output redirection
   */
  AMPL_OUTPUT_CLOSE,
  /**
   * Output of a ``commands`` call into another file
   */
  AMPL_OUTPUT_COMMANDS,
  /**
   * Issued when ``continue`` is encountered
   */
  AMPL_OUTPUT_CONTINUE,
  /**
   * Output of a ``data`` command
   */
  AMPL_OUTPUT_DATA,
  /**
   * Output of a ``delete`` command
   */
  AMPL_OUTPUT_DELETECMD,
  /**
   * Output of a ``drop`` command
   */
  AMPL_OUTPUT_DROP,
  /**
   * Internal
   */
  AMPL_OUTPUT_DROP_OR_RESTORE_ALL,
  /**
   * Else block
   */
  AMPL_OUTPUT_ELSE,
  /**
   * Internal
   */
  AMPL_OUTPUT_ELSE_CHECK,
  /**
   * End of if block
   */
  AMPL_OUTPUT_ENDIF,
  /**
   * Output of a ``environ`` command
   */
  AMPL_OUTPUT_ENVIRON,
  /**
   * Output of a ``fix`` command
   */
  AMPL_OUTPUT_FIX,
  /**
   * Output of a ``for`` command
   */
  AMPL_OUTPUT_FOR,
  /**
   * Output of an ``if`` command
   */
  AMPL_OUTPUT_IF,
  /**
   * Output of a ``let`` command
   */
  AMPL_OUTPUT_LET,
  /**
   * End of loop
   */
  AMPL_OUTPUT_LOOPEND,
  /**
   * Output of an ``objective`` command
   */
  AMPL_OUTPUT_OBJECTIVE,
  /**
   * Occurs when resetting option values
   */
  AMPL_OUTPUT_OPTION_RESET,
  /**
   * Output of a ``printf`` command
   */
  AMPL_OUTPUT_PRINTF,
  /**
   * Output of a ``problem`` command
   */
  AMPL_OUTPUT_PROBLEM,
  /**
   * Output of a ``purge`` command
   */
  AMPL_OUTPUT_PURGE,
  /**
   * Occurs when a right brace is encountered
   */
  AMPL_OUTPUT_RBRACE,
  /**
   * Output of a ``read`` command
   */
  AMPL_OUTPUT_READ,
  /**
   * Output of a ``reload`` command
   */
  AMPL_OUTPUT_RELOAD,
  /**
   * Output of a ``remove`` command
   */
  AMPL_OUTPUT_REMOVE,
  /**
   * Beginning of a repeat loop
   */
  AMPL_OUTPUT_REPEAT,
  /**
   * End of a repeat loop
   */
  AMPL_OUTPUT_REPEAT_END,
  /**
   * Output of a ``reset`` command
   */
  AMPL_OUTPUT_RESET,
  /**
   * Output of a ``restore`` command
   */
  AMPL_OUTPUT_RESTORE,
  /**
   * Internal
   */
  AMPL_OUTPUT_RUN_ARGS,
  /**
   * Internal
   */
  AMPL_OUTPUT_SEMICOLON,
  /**
   * Internal
   */
  AMPL_OUTPUT_SSTEP,
  /**
   * Beginning of the ``then`` part of an if statement
   */
  AMPL_OUTPUT_THEN,
  /**
   * Output of an ``unfix`` command
   */
  AMPL_OUTPUT_UNFIX,
  /**
   * Output of an ``unload`` command
   */
  AMPL_OUTPUT_UNLOAD,
  /**
   * Output of an ``update`` command
   */
  AMPL_OUTPUT_UPDATE,
  /**
   * Output of a ``write`` command
   */
  AMPL_OUTPUT_WRITE
} AMPL_OUTPUTKIND;

/**@}*/


/**
 * \defgroup AMPL_OUTPUTHANDLER AMPL Outputhandler  functions
 * @{
 *
 */

/**
 * @typedef AMPL_OutputHandlerCb
 * @brief Callback type for handling AMPL output messages.
 *
 * This callback is invoked by the AMPL runtime to deliver output generated
 * during model execution, such as solver output, display statements, or
 * informational messages.
 *
 * @param kind   The kind of output being produced (see AMPL_OUTPUTKIND)
 * @param text   Null-terminated output text
 * @param user   User-defined context pointer supplied when the handler
 *               was registered
 */
typedef void (*AMPL_OutputHandlerCb)(AMPL_OUTPUTKIND kind, const char *text, void *user);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_OUTPUT_C_H
