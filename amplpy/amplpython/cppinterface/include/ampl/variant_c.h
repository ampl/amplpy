#ifndef AMPL_VARIANT_C_H
#define AMPL_VARIANT_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>

#include "ampl/declaration_c.h"

/**
 * \defgroup AMPL_VARIANT AMPL Variant struct functions
 * @{
 * The struct can represent a string or a double number, and maps directly to
 * the underlying %AMPL type system.
 *
 */

/**
 * An AMPL variant.
 */
typedef struct AMPL_Variant AMPL_VARIANT;

AMPLAPI void retainVariant(AMPL_VARIANT *v);
AMPLAPI void releaseVariant(AMPL_VARIANT *v);

/**
 * Allocates an empty AMPL_DATAFRAME struct.
 *
 * \param variant Pointer to the pointer of the AMPL_VARIANT struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantCreateEmpty(AMPL_VARIANT **variant);

/**
 * Allocates a numeric AMPL_VARIANT struct.
 *
 * \param variant Pointer to the pointer of the AMPL_VARIANT struct.
 * \param value Numeric value.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantCreateNumeric(AMPL_VARIANT **variant, double value);

/**
 * Allocates a string AMPL_VARIANT struct.
 *
 * \param variant Pointer to the pointer of the AMPL_VARIANT struct.
 * \param cstr String value.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantCreateString(AMPL_VARIANT **variant, const char *cstr);

/**
 * Allocates a copy of an AMPL_VARIANT struct.
 *
 * \param variant Pointer to the pointer of the AMPL_VARIANT struct.
 * \param copy Pointer to the AMPL_VARIANT struct to copy.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantCopy(AMPL_VARIANT **variant, AMPL_VARIANT *copy);

/**
 * Frees the AMPL_VARIANT struct.
 *
 * \param variant Pointer to the pointer of the AMPL_VARIANT struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantFree(AMPL_VARIANT **variant);

/**
 * Compares two AMPL_VARIANT structs.
 *
 * \param v1 Pointer to the first AMPL_VARIANT struct.
 * \param v2 Pointer to the second AMPL_VARIANT struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantCompare(AMPL_VARIANT *v1, AMPL_VARIANT *v2);

/**
 * Get the numeric value of an AMPL_VARIANT struct.
 *
 * \param variant Pointer to the AMPL_VARIANT struct.
 * \param value Pointer to the numeric value.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantGetNumericValue(AMPL_VARIANT *variant, double *value);

/**
 * Get the string value of an AMPL_VARIANT struct.
 *
 * \param variant Pointer to the AMPL_VARIANT struct.
 * \param value Pointer to the string value.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantGetStringValue(AMPL_VARIANT *variant, char **value);

/**
 * Get the type of an AMPL_VARIANT struct.
 *
 * \param variant Pointer to the AMPL_VARIANT struct.
 * \param type Pointer to the type.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantGetType(AMPL_VARIANT *variant, AMPL_TYPE *type);

/**
 * Get the string representation of an AMPL_VARIANT struct.
 *
 * \param variant Pointer to the AMPL_VARIANT struct.
 * \param cstr Pointer to the string representation.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_VariantFormat(AMPL_VARIANT *variant, char **cstr);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_VARIANT_C_H
