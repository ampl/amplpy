#ifndef AMPL_DATAFRAME_C_H
#define AMPL_DATAFRAME_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>

#include "ampl/arg_c.h"
#include "ampl/declaration_c.h"
#include "ampl/errorhandler_c.h"
#include "ampl/tuple_c.h"
#include "ampl/variant_c.h"

/**
 * \defgroup AMPL_DATAFRAME AMPL Dataframe struct functions
 * @{
 * An AMPL_DATAFRAME struct is used to communicate data to and from the %AMPL
 * entities.
 *
 * A struct of AMPL_DATAFRAME can be used to do the following tasks:
 *
 * <ul>
 * <li>Assign values to %AMPL entities (once the AMPL_DATAFRAME is populated,
 * use AMPL_SetData() to assign its values to the modelling entities in its
 * columns) 
 * <li>Get values from %AMPL, decoupling the values from the %AMPL
 * entities they originate via AMPL_EntityGetValues()
 * </ul>
 *
 * <p>
 * An AMPL_DATAFRAME struct can be created in various ways.
 * <ul>
 * <li>Create a skeleton via AMPL_DataFrameCreate(AMPL_DATAFRAME **dataframe,
 * size_t numberOfIndexColumns, size_t numberOfDataColumns,
 * const char *const *headers), specifiying manually the number of indexing
 * columns, the number of data columns and the column headers.
 * <li>Get column names (and number of indexing columns)
 * from entities of the API, using the constructor DataFrame(const EntityArgs
 * &headers). 
 * <li>Get values from AMPL, decoupling the values from the %AMPL
 * entities they originate from (via AMPL_EntityGetValues())
 * </ul>
 * <p>
 * Populating a DataFrame object can be done adding row by row to a pre-existing
 * skeleton via AMPL_DataFrameAddRow(), setting whole columns of a
 * pre-existing skeleton via AMPL_DataFrameSetColumnArg(),
 * AMPL_DataFrameSetColumnArgDouble() and AMPL_DataFrameSetColumnArgString()
 * or adding columns (including indexing columns) via AMPL_DataFrameAddColumn().
 * <p>
 * Modifying a DataFrame object can be done via DataFrame.setColumn method.
 * <p>
 * Accessing data in a DataFrame can be done row by row using
 * DataFrame.getRow() or by column via DataFrame.getColumn().
 */

/**
 * An AMPL Dataframe.
 */
typedef struct AMPL_DataFrame AMPL_DATAFRAME;

/**
 * Allocates the AMPL_DATAFRAME struct.
 *
 * \param dataframe Pointer to the pointer of the AMPL_DATAFRAME struct.
 * \param numberOfIndexColumns Number of index columns.
 * \param numberOfDataColumns Number of data columns.
 * \param headers Column headers.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameCreate(AMPL_DATAFRAME **dataframe,
                                 size_t numberOfIndexColumns,
                                 size_t numberOfDataColumns,
                                 const char *const *headers);

/**
 * Allocates the AMPL_DATAFRAME struct.
 *
 * \param dataframe Pointer to the pointer of the AMPL_DATAFRAME struct.
 * \param numberOfIndexColumns Number of index columns.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameCreate2(AMPL_DATAFRAME **dataframe,
                                  size_t numberOfIndexColumns);

/**
 * Allocates a copy of an AMPL_DATAFRAME struct.
 *
 * \param dataframe Pointer to the pointer of the AMPL_DATAFRAME struct.
 * \param copy Pointer to the AMPL_DATAFRAME struct to copy.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameCopy(AMPL_DATAFRAME **dataframe,
                               AMPL_DATAFRAME *copy);

/**
 * Frees the AMPL_DATAFRAME struct.
 *
 * \param dataframe Pointer to the pointer of the AMPL_DATAFRAME struct.
 */
AMPLAPI void AMPL_DataFrameFree(AMPL_DATAFRAME **dataframe);

/**
 * Get the headers of this DataFrame.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param size Pointer to the size of the headers.
 * \param headers Pointer to array of headers.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetHeaders(AMPL_DATAFRAME *dataframe, size_t *size,
                                     char ***headers);

/**
 * Equality check of DataFrames.
 * 
 * \param df1 Pointer to the first AMPL_DATAFRAME struct.
 * \param df2 Pointer to the second AMPL_DATAFRAME struct.
 * \param equals Pointer to the result of the equality check.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameEquals(AMPL_DATAFRAME *df1, AMPL_DATAFRAME *df2,
                                 int *equals);
/**
 * Get a tabular string representation of the DataFrame.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param output Pointer to the tabular string representation.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameToString(AMPL_DATAFRAME *dataframe, char **output);

/**
 * Reserve space for the given number of rows. NOTE that the rows cannot be
 * accessed, they still have to be added via AMPL_DataFrameAddRow.
 *
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param numRows	Number of rows to be allocated.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameReserve(AMPL_DATAFRAME *dataframe, size_t numRows);

/**
 * Add a row to the DataFrame. The size of the tuple must be equal to the
 * total number of columns in the dataframe.
 * 
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param value	A tuple containing all the values for the row to be added.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameAddRow(AMPL_DATAFRAME *dataframe, AMPL_TUPLE *value);

/**
 * Set the values of a column using AMPL_ARGS.
 * 
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param header The header of the column to be set.
 * \param column The values to set.
 * \param n	The number of items in the column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetColumnArg(AMPL_DATAFRAME *dataframe,
                                       const char *header, AMPL_ARGS *column,
                                       size_t n);

/**
 * Set the values of a double column using doubles.
 * 
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param header The header of the column to be set.
 * \param column The values to set.
 * \param n	The number of items in the column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetColumnArgDouble(AMPL_DATAFRAME *dataframe,
                                             const char *header,
                                             const double *column, size_t n);

/**
 * Set the values of a string column using strings.
 * 
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param header The header of the column to be set.
 * \param column The values to set.
 * \param n	The number of items in the column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetColumnArgString(AMPL_DATAFRAME *dataframe,
                                             const char *header,
                                             const char *const *column,
                                             size_t n);

/**
 * Set the value at the specified row and columnn.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param rowIndex A tuple identiying the row to modify.
 * \param header The header of the column to modify.
 * \param value The value to assign.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetValue(AMPL_DATAFRAME *dataframe,
                                   AMPL_TUPLE *rowIndex, const char *header,
                                   AMPL_VARIANT *value);

/**
 * Set the value at the specified row and columnn.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param rowNumber The 0-based index of the row to modify.
 * \param colNumber The 0-based index of the column to modify (including
 *                 indices).
 * \param value The value to assign.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetValueByIndex(AMPL_DATAFRAME *dataframe,
                                          size_t rowNumber, size_t colNumber,
                                          AMPL_VARIANT *value);

/**
 * Add a new column with the corresponding header and values to the dataframe.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param header The name of the new column header.
 * \param values Pointer to the new column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameAddColumn(AMPL_DATAFRAME *dataframe,
                                    const char *header, AMPL_ARGS *values);

/**
 * Add a new column with the corresponding header and double values to the dataframe.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param header The name of the new column header.
 * \param values Array of doubles representing the new column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameAddColumnDouble(AMPL_DATAFRAME *dataframe,
                                          const char *header,
                                          const double *values);

/**
 * Add a new column with the corresponding header and string values to the dataframe.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param header The name of the new column header.
 * \param values Array of strings representing the new column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameAddColumnString(AMPL_DATAFRAME *dataframe,
                                          const char *header,
                                          const char **values);

/**
 * Add a new empty column with the corresponding header.
 * 
 * \param dataframe	Pointer to the AMPL_DATAFRAME struct.
 * \param header The name of the new columnheader.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameAddEmptyColumn(AMPL_DATAFRAME *dataframe,
                                         const char *header);

/**
 * Get the total number of columns in this dataframe (indexarity + number
 * of values).
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param num Pointer to the number of columns.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetNumCols(AMPL_DATAFRAME *dataframe, size_t *num);

/**
 * Get the number of data rows in this dataframe.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param num Pointer to the number of data rows.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetNumRows(AMPL_DATAFRAME *dataframe, size_t *num);

/**
 * Get the number of indices (the indexarity) of this dataframe.
 *
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param num Pointer to the number of indices needed to access one row of this
 *            dataframe.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetNumIndices(AMPL_DATAFRAME *dataframe, size_t *num);

/**
 * Set the values of a DataFrame from an array of doubles.
 * The DataFrame must have one index and one data column.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param values  An array containing the values to be set.
 * \param l0 The size of the two arrays passed.
 * \param indices0 The indices of the values to set as AMPL_ARGS.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetArray(AMPL_DATAFRAME *dataframe,
                                   const double *values, size_t l0,
                                   AMPL_ARGS *indices0);

/**
 * Set the values of a DataFrame from an array of string literals.
 * The DataFrame must have one index and one data column.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param values An array containing the values to be set
 * \param l0 The size of the two arrays passed.
 * \param indices0 The indices of the values to set
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetArrayString(AMPL_DATAFRAME *dataframe,
                                         const char *const *values, size_t l0,
                                         AMPL_ARGS *indices0);

/**
 * Set a matrix of doubles to an empty DataFrame.
 * The DataFrame must have two indices and one data column.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param values A flattend 2d-array of doubles.
 * \param l0 The size of the first indexing column.
 * \param indices0 The values of the first indexing column.
 * \param l1 The size of the second indexing column.
 * \param indices1 The values of the second indexing column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetMatrix(AMPL_DATAFRAME *dataframe,
                                    const double *values, size_t l0,
                                    AMPL_ARGS *indices0, size_t l1,
                                    AMPL_ARGS *indices1);

/**
 * Set a matrix of strings to an empty DataFrame.
 * The DataFrame must have two indices and one data column.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param values A flattend 2d-array of doubles.
 * \param l0 The size of the first indexing column.
 * \param indices0 The values of the first indexing column.
 * \param l1 The size of the second indexing column.
 * \param indices1 The values of the second indexing column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetMatrixStringString(AMPL_DATAFRAME *dataframe,
                                                const double *values, size_t l0,
                                                const char *const *indices0,
                                                size_t l1,
                                                const char *const *indices1);

/**
 * Set a matrix of strings to an empty DataFrame.
 * The DataFrame must have two indices and one data column.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param values A flattend 2d-array of strings.
 * \param l0 The size of the first indexing column.
 * \param indices0 The values of the first indexing column.
 * \param l1 The size of the second indexing column.
 * \param indices1 The values of the second indexing column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameSetMatrixString(AMPL_DATAFRAME *dataframe,
                                          const char *const *values, size_t l0,
                                          AMPL_ARGS *indices0, size_t l1,
                                          AMPL_ARGS *indices1);

/**
 * Get the column index of a column by its header.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param name The header of the column.
 * \param columnindex Pointer to the index of the column.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetColumnIndex(AMPL_DATAFRAME *dataframe,
                                         const char *name, size_t *columnindex);

/**
 * Get the tuple representation of a row index.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param rowindex The index of the row.
 * \param index Pointer to the tuple representing the index of the row.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetIndexingTuple(AMPL_DATAFRAME *dataframe,
                                           size_t rowindex, AMPL_TUPLE **index);

/**
 * Get a row index by its tuple representation.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param index	Tuple representing the index of the desired row.
 * \param rowindex Pointer to the index of the row.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameGetRowIndex(AMPL_DATAFRAME *dataframe,
                                      AMPL_TUPLE *index, size_t *rowindex);

/**
 * Get the values of a row by its index.
 * 
 * \param dataframe Pointer to the AMPL_DATAFRAME struct.
 * \param rowindex The index of the row.
 * \param colindex The index of the column.
 * \param v Pointer to element.
 * \return Pointer to the AMPL_ERRORINFO struct.
 */
AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameElement(AMPL_DATAFRAME *dataframe, size_t rowindex,
                                  size_t colindex, AMPL_VARIANT **v);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_DATAFRAME_C_H
