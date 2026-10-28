#ifndef AMPL_DECLARATION_C_H
#define AMPL_DECLARATION_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef _WIN32
#ifdef AMPLAPI_EXPORTS
#define AMPLAPI __declspec(dllexport)
#else
#define AMPLAPI __declspec(dllimport)
#endif
#else
#define AMPLAPI __attribute__((visibility("default")))
#endif

/**
 * \defgroup AMPL_TYPE AMPL Type Enumeration
 * @{
 *
 * This enumeration represents the basic value types supported by the AMPL
 * C API. It mirrors the underlying AMPL type system and is used to describe
 * the runtime type of scalar values returned by the API (for example, option
 * values, parameter values, or expression results).
 *
 * The enum distinguishes between numeric values, string values, and the
 * absence of a value.
 *
 */

/** Enumeration of the basic value types supported by the AMPL C API. */
typedef enum {
  /**
   * No value is present.
   * This is typically used to indicate an uninitialized value or an empty
   * result.
   */
  AMPL_EMPTY,

  /**
   * A numeric value represented as a double-precision floating point number.
   */
  AMPL_NUMERIC,

  /**
   * A string value represented as a null-terminated UTF-8 string.
   */
  AMPL_STRING
} AMPL_TYPE;

/**@}*/

/**
 * \defgroup AMPL_SUFFIX AMPL Suffix
 * @{
 *
 * \brief Suffixes available on AMPL entities and instances.
 *
 * This group contains enumerations defining the string and numeric
 * suffixes that can be queried on AMPL entities such as variables,
 * constraints, objectives, sets, and parameters.
 *
 * In AMPL, a suffix represents additional information associated with
 * an entity or a specific instance of that entity. Typical examples
 * include:
 * - primal values
 * - dual values (shadow prices)
 * - bounds
 * - slacks
 * - reduced costs
 * - solver status information
 *
 * The C API provides functions such as:
 * - AMPL_InstanceGetDoubleSuffix()
 * - AMPL_InstanceGetIntSuffix()
 * - AMPL_InstanceGetStringSuffix()
 *
 * to retrieve suffix values programmatically.
 *
 * Suffixes are divided into:
 * - string-valued suffixes (see ::AMPL_STRINGSUFFIX)
 * - numeric-valued suffixes (see ::AMPL_NUMERICSUFFIX)
 *
 */


/**
 * \brief String-valued suffixes available on AMPL entities and instances.
 *
 * These suffixes return string information associated with variables,
 * constraints, and objectives (e.g., solver statuses or messages).
 */
typedef enum {
  /** Solver status of the individual entity (e.g., basic, nonbasic). */
  AMPL_ASTATUS,

  /** Solver status in symbolic/string form. */
  AMPL_SSTATUS,

  /** Solve status of the model or entity. */
  AMPL_STATUS,

  /** Message returned by the solver. */
  AMPL_MESSAGE,

  /** Result string returned by the solver. */
  AMPL_RESULT,

  /** Optimization sense of an objective (e.g., "minimize", "maximize"). */
  AMPL_SENSE 
} AMPL_STRINGSUFFIX;


/**
 * \brief Numeric suffixes available on AMPL entities and instances.
 *
 * These suffixes return numeric values associated with variables,
 * constraints, and objectives, such as primal values, dual values,
 * bounds, slacks, and reduced costs.
 */
typedef enum {

  /* ===================== */
  /* Common entity suffixes */
  /* ===================== */

  /** Current value of the entity (primal value). */
  AMPL_VALUE,

  /** Defined equation value. */
  AMPL_DEFEQN,

  /** Dual value (shadow price). */
  AMPL_DUAL,

  /** Initial value provided by the user. */
  AMPL_INIT,

  /** Default initial value. */
  AMPL_INIT0,

  /** Lower bound. */
  AMPL_LB,

  /** Upper bound. */
  AMPL_UB,

  /** Original lower bound. */
  AMPL_LB0,

  /** Original upper bound. */
  AMPL_UB0,

  /** First lower bound (multi-bound context). */
  AMPL_LB1,

  /** First upper bound (multi-bound context). */
  AMPL_UB1,

  /** Second lower bound (multi-bound context). */
  AMPL_LB2,

  /** Second upper bound (multi-bound context). */
  AMPL_UB2,

  /** Lower reduced cost. */
  AMPL_LRC,

  /** Upper reduced cost. */
  AMPL_URC,

  /** Lower slack value. */
  AMPL_LSLACK,

  /** Upper slack value. */
  AMPL_USLACK,

  /** Reduced cost. */
  AMPL_RC,

  /** Slack value. */
  AMPL_SLACK,

  /* ============ */
  /* Constraints  */
  /* ============ */

  /** Constraint body value. */
  AMPL_BODY,

  /** Defined variable value (for defined constraints). */
  AMPL_DEFVAR,

  /** Dual initial value. */
  AMPL_DINIT,

  /** Default dual initial value. */
  AMPL_DINIT0,

  /** Lower bound slack. */
  AMPL_LBS,

  /** Upper bound slack. */
  AMPL_UBS,

  /** Lower dual value. */
  AMPL_LDUAL,

  /** Upper dual value. */
  AMPL_UDUAL,

  /** Value for logical constraints. */
  AMPL_VAL,

  /* ============ */
  /* Objectives   */
  /* ============ */

  /** Solver exit code for the objective. */
  AMPL_EXITCODE

} AMPL_NUMERICSUFFIX;

/**@}*/


/**
 * \defgroup AMPL_BUILTINPARAM AMPL Built-in Parameters
 * @{
 *
 * \brief Built-in AMPL parameters.
 *
 * This group contains enumerations representing predefined AMPL parameters
 * that can be queried through the C API using functions such as
 * AMPL_GetBuiltInParameter().
 *
 * Built-in parameters provide information about the state of the AMPL
 * interpreter and the most recent solve operation. In particular,
 * they expose timing statistics such as CPU time, system time,
 * user time, and elapsed (wall-clock) time.
 *
 * These parameters are read-only and reflect values maintained internally
 * by AMPL.
 *
 */


/**
 * \brief Built-in AMPL parameters providing solve timing information.
 *
 * These parameters provide timing statistics for the most recent solve
 * and cumulative solve operations.
 */
typedef enum {

  /** CPU time spent in the solver. */
  SOLVE_TIME,

  /** System CPU time spent in the solver. */
  SOLVE_SYSTEM_TIME,

  /** User CPU time spent in the solver. */
  SOLVE_USER_TIME,

  /** Elapsed (wall-clock) time for the solver. */
  SOLVE_ELAPSED_TIME,

  /** Total accumulated solver CPU time. */
  TOTAL_SOLVE_TIME,

  /** Total accumulated solver system CPU time. */
  TOTAL_SOLVE_SYSTEM_TIME,

  /** Total accumulated solver user CPU time. */
  TOTAL_SOLVE_USER_TIME,

  /** Total accumulated solver elapsed (wall-clock) time. */
  TOTAL_SOLVE_ELAPSED_TIME

} AMPL_BUILTINPARAMETER;

/**@}*/


#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_DECLARATION_C_H
