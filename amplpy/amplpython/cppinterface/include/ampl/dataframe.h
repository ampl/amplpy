#ifndef AMPL_DATAFRAME_H
#define AMPL_DATAFRAME_H

#include "ampl/ampl_c.h"
#include "ampl/arg.h"
#include "ampl/declarations.h"
#include "ampl/macros.h"
#include "ampl/slice.h"
#include "ampl/string.h"
#include "ampl/tuple.h"

namespace ampl {

class EntityArgs;

/**
 * A DataFrame object, used to communicate data to and from the %AMPL entities.
 *
 * An object of this class can be used to do the following tasks:
 *
 * <ul>
 * <li>Assign values to %AMPL entities (once the DataFrame is populated, use
 * AMPL::setData() to assign its values to the modelling entities in
 * its columns)
 * <li>Get values from %AMPL, decoupling the values from the %AMPL entities they
 * originate via Entity::getValues()
 * </ul>
 *
 * <p>
 * A DataFrame object can be created in various ways.
 * <ul>
 * <li>Create a skeleton via DataFrame(std::size_t numberOfIndexColumns,
 * StringArgs headers), specifiying manually the number of indexing columns and
 * the column headers. <li>Get column names (and number of indexing columns)
 * from entities of the API, using the constructor DataFrame(const EntityArgs
 * &headers). <li>Get values from AMPL, decoupling the values from the %AMPL
 * entities they originate from (via Entity::getValues())
 * </ul>
 * <p>
 * Populating a DataFrame object can be done adding row by row to a pre-existing
 * skeleton via DataFrame.addRow(), setting whole columns of a
 * pre-existing skeleton via DataFrame.setColumn() or adding columns
 * (including indexing columns) via DataFrame.addColumn().
 * <p>
 * Modifying a DataFrame object can be done via DataFrame.setColumn method.
 * <p>
 * Accessing data in a DataFrame can be done row by row using
 * DataFrame.getRow() or by column via DataFrame.getColumn().
 */
class DataFrame {
 public:
  /**
  Represents a row in a DataFrame
  */
  typedef Slice<true> Row;
  /**
  Represents a column in a DataFrame
  */
  typedef Slice<false> Column;

  /**
   * Create a new DataFrame with the specified number of indices.
   */
  explicit DataFrame(int numberOfIndexColumns) {
    AMPL_CALL_CPP_W_FREE(AMPL_DataFrameCreate2(&impl_, numberOfIndexColumns));
  }

  /**
  Destructor
  */
  ~DataFrame() { AMPL_DataFrameFree(&impl_); }

  /**
   Create a new DataFrame where the specified number of columns are an index
   and with the specified strings as column headers.

   \param numberOfIndexColumns
              Number of columns to be considered as index for this table (>=0)
   \param headers
              The columns headers to be used
  @throws std::invalid_argument
               If a non-valid number of indices is specified (e.g. > than the
                         number of headers)
  */
  DataFrame(std::size_t numberOfIndexColumns, StringArgs headers) {
    if (numberOfIndexColumns > headers.size())
      throw std::invalid_argument("Invalid number of indices.");
    AMPL_CALL_CPP_W_FREE(AMPL_DataFrameCreate(&impl_, numberOfIndexColumns, headers.size() - numberOfIndexColumns, headers.args()));
  }

  /**
  * Create a new DataFrame with the specified entities as column headers.
  *
  * \param headers
  *            The columns headers to be used; since they are %AMPL entities,
  *            sets are automatically considered indices and have to be
  *            placed first in the constructor. The
  * @throws std::invalid_argument
  *           if sets are not put first while using this constructor or if the
                          indexarity of the data columns does not correspond to
                                                  the total indexarity of the
  DataFrame
  */
  explicit DataFrame(const EntityArgs& headers);

  /**
  Copy constructor (deep copy)
  */
  DataFrame(const DataFrame& other) {
    AMPL_CALL_CPP_W_FREE(AMPL_DataFrameCopy(&impl_, other.impl_));
  }

  explicit DataFrame(AMPL_DATAFRAME *other) : impl_(other) { }

  /**
  Assignment operator (deep copies all the data)
  */
  DataFrame& operator=(const DataFrame& df) {
    if (this != &df) {
      AMPL_DATAFRAME* newDf;
      AMPL_CALL_CPP(AMPL_DataFrameCopy(&newDf, df.impl_));
      AMPL_DataFrameFree(&impl_);
      impl_ = newDf;
    }
    return *this;
  }

  /**
  Equality check
  */
  bool operator==(const DataFrame& other) const {
    int equals;
    AMPL_CALL_CPP(AMPL_DataFrameEquals(impl_, other.impl_, &equals));
    return equals != 0;
  }

  /**
  Inequality check
  */
  bool operator!=(const DataFrame& other) const {
    int equals;
    AMPL_CALL_CPP(AMPL_DataFrameEquals(impl_, other.impl_, &equals));
    return equals == 0;
  }

  /**
   Get the total number of columns in this dataframe (indexarity + number
   of values)
   \return	The number of columns.
   */
  std::size_t getNumCols() const {
    size_t num;
    AMPL_CALL_CPP(AMPL_DataFrameGetNumCols(impl_, &num));
    return num;
  }

  /**
   Get the number of data rows in this dataframe.
   \return	The number of rows.
   */
  std::size_t getNumRows() const {
    size_t num;
    AMPL_CALL_CPP(AMPL_DataFrameGetNumRows(impl_, &num));
    return num;
  }

  /**
   Get the number of indices (the indexarity) of this dataframe.
   \return	The number of indices needed to access one row of this
   dataframe.
   */
  std::size_t getNumIndices() const {
    size_t num;
    AMPL_CALL_CPP(AMPL_DataFrameGetNumIndices(impl_, &num));
    return num;
  }

  /**
   Add a row to the DataFrame. The size of the tuple must be equal to the
   total number of columns in the dataframe.
   \param	value	A tuple containing all the values for the row to be
   added.
   */
  void addRow(Tuple value) {
    AMPL_CALL_CPP(AMPL_DataFrameAddRow(impl_, value.impl()));
  }

  /**
   Add a value to a DataFrame composed of only one column.
   \param	a1	The value to be added.
   */
  void addRow(Variant a1) {
    Tuple arg(a1);
    addRow(arg);
  }

  /**
  Add a value to a DataFrame composed of two columns.
  \param	a1 The value to be added in the first column.
  \param	a2 The value to be added in the second column.
  */
  void addRow(Variant a1, Variant a2) {
    Tuple arg(a1, a2);
    addRow(arg);
  }

  /**
  Add a value to a DataFrame composed of three columns.
  \param	a1 The value to be added in the first column.
  \param	a2 The value to be added in the second column.
  \param	a3 The value to be added in the third column.
  */
  void addRow(Variant a1, Variant a2, Variant a3) {
    Tuple arg(a1, a2, a3);
    addRow(arg);
  }

  /**
  Add a value to a DataFrame composed of four columns.
  \param	a1 The value to be added in the first column.
  \param	a2 The value to be added in the second column.
  \param	a3 The value to be added in the third column.
  \param	a4 The value to be added in the fourth column.
  */
  void addRow(Variant a1, Variant a2, Variant a3, Variant a4) {
    Tuple arg(a1, a2, a3, a4);
    addRow(arg);
  }

  /**
   Reserve space for the given number of rows. NOTE that the rows cannot be
   accessed, they still have to be added via DataFrame::addRow.
   \param	numRows	Number of rows to be allocated.
   */
  void reserve(std::size_t numRows) {
    AMPL_CALL_CPP(AMPL_DataFrameReserve(impl_, numRows));
  }

  /**
   Give a tabular string representation of the dataframe object.
   \return	A std::string that represents this object
   */
  std::string toString() const {
    char *output;
    AMPL_CALL_CPP(AMPL_DataFrameToString(impl_, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   Add a new empty column with the corresponding header.
   \param	header	The header.
   */
  void addColumn(fmt::CStringRef header) {
    AMPL_CALL_CPP(AMPL_DataFrameAddEmptyColumn(impl_, header.c_str()));
  }

  /**
   * Add a new column with the corresponding header and values to the dataframe
   * \param header The name of the new column
   * \param values An array of size getNumRows() with all the values of the new
   * row
   */
  void addColumn(fmt::CStringRef header, Args values) {
    AMPL_CALL_CPP(AMPL_DataFrameAddColumn(impl_, header.c_str(), values.data()));
  }

  /**
   * Get the specified column as a view object
   * \param	header	The header of the column.
   */
  Column getColumn(fmt::CStringRef header) const {
    size_t i;
    AMPL_CALL_CPP(AMPL_DataFrameGetColumnIndex(impl_, header.c_str(), &i));

    return Column(impl_, i);
  }
  /**
   * Set the value at the specified row and columnn
   * \param rowIndex A tuple identiying the row to modify
   * \param colHeader The header of the column to modify
   * \param value The value to assign
   */
  void setValue(Tuple rowIndex, fmt::CStringRef colHeader,
                ampl::Variant value) {
    AMPL_CALL_CPP(AMPL_DataFrameSetValue(impl_, rowIndex.impl(), colHeader.c_str(), value.impl()));
  }

  /**
   * Set the value at the specified row and columnn
   * \param rowIndex The 0-based index of the row to modify
   * \param colIndex The 0-based index of the column to modify (including
   * indices) \param value The value to assign
   */
  void setValue(std::size_t rowIndex, size_t colIndex, ampl::Variant value) {
    AMPL_CALL_CPP(AMPL_DataFrameSetValueByIndex(impl_, rowIndex, colIndex, value.impl()));
  }

  /**
   * Set the values of a column
   * \param	header	The header of the column to be set
   * \param	column	The values to set.
   * \param n		The number of items in the column.
   */
  void setColumn(fmt::CStringRef header, Args column, std::size_t n) {
    AMPL_CALL_CPP(AMPL_DataFrameSetColumnArg(impl_, header.c_str(), column.data(), n));
  }

  /**
   * Get row by numeric index.
   * \param	index	Zero-based index of the row to get
   * \return	The corresponding row.
   */
  Row getRowByIndex(std::size_t index) const {
    if (index >= getNumRows()) throw std::out_of_range("Index out of range.");
    return Row(impl_, index);
  }

  /**
  * Get a row by value of the indexing column
   (for DataFrames with one indexing column)
  * \param	a1 Index of the desired row
  * \return	The correponding row.
  */
  Row getRow(Variant a1) {
    Variant args[] = {a1};
    return getRow(Tuple(args, 1));
  }

  /**
   * Get a row by value of the indexing columns.
   * If the index is not specified, gets the only row of a dataframe
   * with no indexing columns.
   * \param	index	Tuple representing the index of the desired row
   * \return	The row.
   */
  Row getRow(Tuple index = Tuple()) const {
    size_t i;
    AMPL_CALL_CPP(AMPL_DataFrameGetRowIndex(impl_, index.impl(), &i));

    if (i == getNumRows())
      throw std::out_of_range("A row with the specified index does not exist.");
    return Row(impl_, i);
  }
#ifndef SWIG
  /**
   * Iterates through the DataFrame in a row-by-row fashion
   */ 
  class iterator {
   public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = Row;
    using difference_type = std::ptrdiff_t;
    using pointer = value_type*;
    using reference = value_type&;

   private:
    friend class DataFrame;
    AMPL_DATAFRAME* ptr_;
    std::size_t index_;

    iterator(AMPL_DATAFRAME* ptr, std::size_t index)
        : ptr_(ptr), index_(index) {}

   public:
    /**
     * Dereferences the iterator, gets a DataFrame::Row
     */
    value_type operator*() const { return Row(ptr_, index_); }

    /**
     * Go to the next row
     */
    iterator& operator++() {
      index_++;
      return *this;
    }

    /**
     * Go to the next row
     */
    iterator operator++(int) {
      iterator clone(*this);
      index_++;
      return clone;
    }

    /**
     * Equality check
     */
    bool operator==(iterator other) const {
      assert(ptr_ == other.ptr_);
      return (index_ == other.index_);
    }

    /**
     * Inequality check
     */
    bool operator!=(iterator other) const { return !(*this == other); }
  };

  /**
   * Get the iterator to the first row in this DataFrame
   */
  iterator begin() const { return iterator(impl_, 0); }

  /**
   * Get the iterator to the last row in this DataFrame (an iterator
   * of numerical index DataFrame::getNumRows).
   */
  iterator end() const { return iterator(impl_, getNumRows()); }

  /**
   * Get the iterator to the specified row in this DataFrame.
   * \param index The index of the Row to be found
   * \return An iterator pointing to the found row, or iterator::end if not
   * found.
   */
  iterator find(Tuple index) const {
    size_t i;
    AMPL_CALL_CPP(AMPL_DataFrameGetRowIndex(impl_, index.impl(), &i));
    return iterator(impl_, i);
  }
#endif

  /**
   * Get the headers of this DataFrame
   * \return	The headers of this DataFrame
   */
  StringArray getHeaders() const {
    std::size_t size;
    char **ref;
    AMPL_CALL_CPP(AMPL_DataFrameGetHeaders(impl_, &size, &ref));
    const char **strings_ = new const char*[size];
    for (std::size_t i = 0U; i < size; i++) {
        size_t length = strlen(ref[i]) + 1;
        char* new_str = new char[length];
#ifdef _WIN32
        strncpy_s(new_str, length+1, ref[i], _TRUNCATE);
#else
        strncpy(new_str, ref[i], length);
#endif
        strings_[i] = new_str;
    }
    StringArray headers = StringArray(strings_, size);
    for (size_t i = 0; i < size; ++i) AMPL_StringFree(&ref[i]);
    free(ref);
    for (std::size_t i = 0U; i < size; i++) {
      delete[] strings_[i];
    }
    delete[] strings_;
    return headers;
  }

  /**
   * Set the values of a DataFrame from an array of doubles.
   * The DataFrame must have one index and one data column.
   * \param indices The indices of the values to set
   * \param values  An array containing the values to be set
   */
  template <std::size_t NR>
  void setArray(Args indices, const double (&values)[NR]) {
    AMPL_CALL_CPP(AMPL_DataFrameSetArray(impl_, values, NR, indices.data()));
  }
#ifndef SWIG
  /**
   * Set the values of a DataFrame from an array of string literals.
   * The DataFrame must have one index and one data column.
   * \param indices The indices of the values to set
   * \param values  An array containing the values to be set
   */
  template <std::size_t NR>
  void setArray(Args indices, const char* (&values)[NR]) {
    AMPL_CALL_CPP(AMPL_DataFrameSetArrayString(impl_, values, NR, indices.data()));
  }
#endif
  /**
   * Set the values of a DataFrame from an array of doubles.
   * The DataFrame must have one index and one data column.
   * \param size The size of the two arrays passed
   * \param indices The indices of the values to set
   * \param values  An array containing the values to be set
   */
  void setArray(std::size_t size, Args indices,
                const double* values) {
    AMPL_CALL_CPP(AMPL_DataFrameSetArray(impl_, values, size, indices.data()));
  }

  /**
   * Set the values of a DataFrame from an array of string literals.
   * The DataFrame must have one index and one data column.
   * \param size The size of the two arrays passed
   * \param indices The indices of the values to set
   * \param values  An array containing the values to be set
   */
  void setArray(std::size_t size, Args indices,
                const char* const* values) {
    AMPL_CALL_CPP(AMPL_DataFrameSetArrayString(impl_, values, size, indices.data()));
  }

  /**
   * Set a matrix of doubles to an empty DataFrame.
   * The DataFrame must have two indices and one data column.
   * \param indices0 The values of the first indexing column
   * \param indices1 The values of the second indexing column
   * \param values a 2d-array of doubles
   */
  template <std::size_t NR, std::size_t NC>
  void setMatrix(Args indices0, Args indices1,
                 const double (&values)[NR][NC]) {
    AMPL_CALL_CPP(AMPL_DataFrameSetMatrix(
        impl_, reinterpret_cast<const double*>(values), NR, indices0.data(), NC,
        indices1.data()));
  }
#ifndef SWIG
  /**
   * Set a matrix of strings to an empty DataFrame.
   * The DataFrame must have two indices and one data column.
   * \param indices0 The values of the first indexing column
   * \param indices1 The values of the second indexing column
   * \param values a 2d-array of string literals
   */
  template <std::size_t NR, std::size_t NC>
  void setMatrix(Args indices0, Args indices1,
                 const char* (&values)[NR][NC]) {
    AMPL_CALL_CPP(AMPL_DataFrameSetMatrixString(impl_, reinterpret_cast<const char* const*>(values), NR, indices0.data(), NC,
                                  indices1.data()));
  }
#endif
  /**
   * Set a matrix of doubles to an empty DataFrame.
   * The DataFrame must have two indices and one data column.
   * \param num_rows The size of the first dimension (number of rows)
   * \param row_indices The values of the first indexing column
   * \param num_cols The size of the second dimension (number of columns)
   * \param indices_cols The values of the second indexing column
   * \param values a 2d-array of doubles
   */
  void setMatrix(std::size_t num_rows, Args row_indices,
                 std::size_t num_cols, Args indices_cols,
                 const double* values) {
    AMPL_CALL_CPP(AMPL_DataFrameSetMatrix(
        impl_, values, num_rows, row_indices.data(), num_cols,
        indices_cols.data()));
  }

  /**
   * Set a matrix of string literals to an empty DataFrame.
   * The DataFrame must have two indices and one data column.
   * \param num_rows The size of the first dimension (number of rows)
   * \param row_indices The values of the first indexing column
   * \param num_cols The size of the second dimension (number of columns)
   * \param indices_cols The values of the second indexing column
   * \param values a 2d-array of strings
   */
  void setMatrix(std::size_t num_rows, Args row_indices,
                 std::size_t num_cols, Args indices_cols,
                 const char* const* values) {
    AMPL_CALL_CPP(AMPL_DataFrameSetMatrixString(
        impl_, values, num_rows, row_indices.data(), num_cols,
        indices_cols.data()));
  }

  /**
   * Infrastructure: returns a pointer to the inner object.
   */
  AMPL_DATAFRAME* impl() const { return impl_; }

 private:
  AMPL_DATAFRAME *impl_;
};

}  // namespace ampl

#include "ampl/entity.h"  // NOTE: keep this line out of "namespace ampl"
                          // in order to avoid very long STL error messages

namespace ampl {

inline DataFrame::DataFrame(const EntityArgs& headers) {
  if (headers.size() == 0)
    throw std::invalid_argument("Cannot have a DataFrame without headers.");
  std::vector<const char*> names(headers.size());
  for (std::size_t i = 0; i < headers.size(); i++) {
    names[i] = headers.getArgs()[i].name_.c_str();
  }
  AMPL_CALL_CPP_W_FREE(AMPL_DataFrameCreate3(&impl_, headers.getArgs()[0].ampl_, names.data(), names.size()));
}

}  // namespace ampl

#endif  // AMPL_DATAFRAME_H
