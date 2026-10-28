#ifndef AMPL_ERRORHANDLER_C_H
#define AMPL_ERRORHANDLER_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>

#include "ampl/declaration_c.h"

/**
 * \defgroup AMPL_ERRORHANDLER AMPL Errorhandler functions
 * @{
 * These fuctions provide error infos of the underlying AMPL interpreter. 
 *
 */

/**
 * @enum AMPL_ERRORCODE
 * @brief Enumerates all possible error and exception types reported by AMPL.
 *
 * These error codes classify the nature of errors returned by AMPL API calls
 * and error handlers, ranging from syntax and runtime errors to licensing
 * and infeasibility issues.
 */
typedef enum {
  /** Generic exception */
  AMPL_EXCEPTION = 0,

  /** Licensing-related error */
  AMPL_LICENSE_EXCEPTION,

  /** File input/output error */
  AMPL_FILE_IO_EXCEPTION,

  /** Unsupported or invalid operation */
  AMPL_UNSUPPORTED_OPERATION_EXCEPTION,

  /** Invalid subscript or index usage */
  AMPL_INVALID_SUBSCRIPT_EXCEPTION,

  /** Syntax error in AMPL code */
  AMPL_SYNTAX_ERROR_EXCEPTION,

  /** Missing or unavailable data */
  AMPL_NO_DATA_EXCEPTION,

  /** Logical error in model or API usage */
  AMPL_LOGIC_ERROR,

  /** Runtime error during model execution */
  AMPL_RUNTIME_ERROR,

  /** Invalid argument passed to an API function */
  AMPL_INVALID_ARGUMENT,

  /** Argument value out of allowable range */
  AMPL_OUT_OF_RANGE,

  /** Standard library exception */
  AMPL_STD_EXCEPTION,

  /** Error during presolve phase */
  AMPL_PRESOLVE_EXCEPTION,

  /** Model infeasibility detected */
  AMPL_INFEASIBILITY_EXCEPTION
} AMPL_ERRORCODE;

/**
 * @struct AMPL_ErrorInfo
 * @brief Opaque structure holding detailed error information.
 *
 * Instances of this structure are returned by AMPL API calls when
 * an error or warning occurs. Access its contents only via the
 * provided accessor functions.
 */
/** Opaque handle to an AMPL error info object returned by API calls. */
typedef struct AMPL_ErrorInfo AMPL_ERRORINFO;

/**
 * @def AMPL_CALL
 * @brief Helper macro to invoke an AMPL API call and report errors.
 *
 * This macro evaluates an expression expected to return an
 * AMPL_ERRORINFO pointer. If an error is returned, its message
 * is printed to standard error.
 *
 * @param x An expression returning `AMPL_ERRORINFO*`
 *
 * @note This macro does not terminate execution or free the error object.
 */
#define AMPL_CALL(x)                                                 \
    do {                                                             \
        AMPL_ERRORINFO *call = (x);                                  \
        if (call) {                                                  \
            fprintf(stderr, "%s\n", AMPL_ErrorInfoGetMessage(call)); \
            AMPL_ErrorInfoFree(&call);                               \
        }                                                            \
    }                                                                \
    while(0)

/**
 * @brief Retrieve the error code associated with an error.
 *
 * @param error Pointer to an AMPL_ERRORINFO instance
 * @return The corresponding AMPL_ERRORCODE
 */
AMPLAPI AMPL_ERRORCODE AMPL_ErrorInfoGetError(AMPL_ERRORINFO *error);

/**
 * @brief Retrieve the human-readable error message.
 *
 * @param error Pointer to an AMPL_ERRORINFO instance
 * @return Null-terminated string describing the error
 */
AMPLAPI char *AMPL_ErrorInfoGetMessage(AMPL_ERRORINFO *error);

/**
 * @brief Retrieve the line number where the error occurred.
 *
 * @param error Pointer to an AMPL_ERRORINFO instance
 * @return Line number, or -1 if unavailable
 */
AMPLAPI int AMPL_ErrorInfoGetLine(AMPL_ERRORINFO *error);

/**
 * @brief Retrieve the character offset within the line.
 *
 * @param error Pointer to an AMPL_ERRORINFO instance
 * @return Character offset, or -1 if unavailable
 */
AMPLAPI int AMPL_ErrorInfoGetOffset(AMPL_ERRORINFO *error);

/**
 * @brief Retrieve the source text associated with the error.
 *
 * This may contain the line of AMPL code that triggered the error.
 *
 * @param error Pointer to an AMPL_ERRORINFO instance
 * @return Null-terminated source string, or NULL if unavailable
 */
AMPLAPI char *AMPL_ErrorInfoGetSource(AMPL_ERRORINFO *error);

/**
 * @brief Free an AMPL_ERRORINFO object.
 *
 * This function releases all resources associated with the error
 * and sets the pointer to NULL.
 *
 * @param error Address of an AMPL_ERRORINFO pointer
 * @return 0 on success, non-zero on failure
 */
AMPLAPI int AMPL_ErrorInfoFree(AMPL_ERRORINFO **error);

/**
 * @typedef ErrorHandlerCbPtr
 * @brief Callback type for custom error and warning handling.
 *
 * This callback can be registered to receive detailed information
 * about errors and warnings produced by AMPL.
 *
 * @param isWarning True if the message is a warning, false if it is an error
 * @param filename Source file where the issue occurred (may be NULL)
 * @param row Line number in the source file
 * @param offset Character offset within the line
 * @param message Human-readable message
 * @param errorHandler User-defined context pointer
 */
typedef void (*ErrorHandlerCbPtr)(bool isWarning,
                                 const char* filename,
                                 int row,
                                 int offset,
                                 const char* message,
                                 void* errorHandler);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* AMPL_ERRORHANDLER_C_H */
