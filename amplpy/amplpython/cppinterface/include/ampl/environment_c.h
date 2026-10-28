#ifndef AMPL_ENVIRONMENT_C_H
#define AMPL_ENVIRONMENT_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>

#include "ampl/declaration_c.h"

/**
 * \defgroup AMPL_ENVIRONMENT AMPL Environment functions
 * @{
 * These fuctions provide access to the environment variables and provides facilities to specify where to load the underlying AMPL interpreter. 
 *
 */

/**
 * \struct AMPL_ENVIRONMENTVAR
 *
 * Represents a single environment variable used by the AMPL C API.
 *
 * This structure stores a name–value pair corresponding to an environment
 * variable. It is typically used to configure or customize the execution
 * environment of the underlying AMPL interpreter, for example to control
 * library paths, licensing, or runtime behavior.
 *
 * The strings referenced by this structure are expected to be
 * null-terminated. Ownership and lifetime of the strings are managed by
 * the caller unless explicitly stated otherwise.
 */
typedef struct {
  /** Name of the environment variable. */
  char *name;
  /** Value assigned to the environment variable. */
  char *value;
} AMPL_ENVIRONMENTVAR;

/**
 * Get the name of an environment variable.
 *
 * \param envvar Pointer to the AMPL_ENVIRONMENTVAR struct.
 * \param name Pointer to the string where the variable name will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentVarGetName(AMPL_ENVIRONMENTVAR *envvar, char **name);

/**
 * Get the value of an environment variable.
 *
 * \param envvar Pointer to the AMPL_ENVIRONMENTVAR struct.
 * \param value Pointer to the string where the variable value will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentVarGetValue(AMPL_ENVIRONMENTVAR *envvar, char **value);


/**
 * An AMPL Environment.
 */
typedef struct AMPL_Environment AMPL_ENVIRONMENT;

/**
 * Allocates the AMPL_ENVIRONMENT struct with ability to select the location of the AMPL binary. 
 * Note that if this function is used, the automatic lookup for an AMPL executable will not be executed.
 *
 * \param env Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory The directory in which to look for the AMPL binary.
 * \param binaryName The name of the AMPL executable if other than “ampl”.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentCreate(AMPL_ENVIRONMENT **env, const char *binaryDirectory, const char *binaryName);

/**
 * Frees the AMPL_ENVIRONMENT struct.
 *
 * \param env Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentFree(AMPL_ENVIRONMENT **env);

/**
 * Allocates a copy of an AMPL_ENVIRONMENT struct.
 *
 * \param copy Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \param src Pointer to the AMPL_ENVIRONMENT struct to copy.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentCopy(AMPL_ENVIRONMENT **copy, AMPL_ENVIRONMENT *src);

/**
 * Add an environment variable to the environment, or change its value if already defined.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param name The name of the environment variable.
 * \param value The value of the environment variable.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentAddEnvironmentVariable(AMPL_ENVIRONMENT *env, const char *name, const char *value);

/**
 * Get the location where AMPLAPI will search for the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory Pointer to the string where the binary directory will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentGetBinaryDirectory(AMPL_ENVIRONMENT *env, char **binaryDirectory);

/**
 * Get the interpreter that will be used for an AMPL struct constructed
 * using this environment
 * 
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param amplCommand Pointer to the string where the interpreter will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentGetAMPLCommand(AMPL_ENVIRONMENT *env, char **amplCommand);

/**
 * Set the location where AMPLAPI will search for the AMPL executable. 
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory The directory in which to search for the AMPL executable.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentSetBinaryDirectory(AMPL_ENVIRONMENT *env, const char *binaryDirectory);

/**
 * Get the name of the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryName Pointer to the string where the executable name will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentGetBinaryName(AMPL_ENVIRONMENT *env, char **binaryName);

/**
 * Set the name of the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryName The name of the AMPL executable.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentSetBinaryName(AMPL_ENVIRONMENT *env, const char *binaryName);

/**
 * Store all variables into string.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param str Pointer to the string where the environment variables will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentToString(AMPL_ENVIRONMENT *env, char **str);

/**
 * Get the size of the environment variables.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param size Pointer to the size of the environment variables will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentGetSize(AMPL_ENVIRONMENT *env, size_t *size);

/**
 * Get the first environment variable in the environment.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param envvar Pointer to the AMPL_ENVIRONMENTVAR pointer where the result will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentGetEnvironmentVar(AMPL_ENVIRONMENT *env, AMPL_ENVIRONMENTVAR **envvar);

/**
 * Find an environment variable by name.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param name Name of the environment variable to find.
 * \param envvar Pointer to the AMPL_ENVIRONMENTVAR pointer where the result will be stored.
 * \return 0 on success, non-zero on failure.
 */
AMPLAPI int AMPL_EnvironmentFindEnvironmentVar(AMPL_ENVIRONMENT *env, const char *name, AMPL_ENVIRONMENTVAR **envvar);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_ENVIRONMENT_C_H
