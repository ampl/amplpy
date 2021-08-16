namespace ampl {
  namespace internal{
    template <bool ROW> class Slice {
    public:
      class iterator {
      public:
        bool operator==(const iterator &other) const;
        bool operator!=(const iterator &other) const;
        VariantRef operator*() const;
        iterator &operator=(const iterator &other);
        iterator &operator++();
        iterator operator++(int);
      };
      std::size_t size() const;
      iterator begin() const;
      iterator end() const;
      VariantRef operator[](std::size_t index) const;
    };
  } // internal
} // ampl

%ignore ampl::DataFrame::DataFrame(std::size_t numberOfIndexColumns, StringArgs headers);
%ignore ampl::DataFrame::addColumn;
%ignore ampl::DataFrame::setArray;
%ignore ampl::DataFrame::setColumn;
%ignore ampl::DataFrame::setMatrix;
%ignore ampl::DataFrame::setValue;

%include "ampl/dataframe.h"


%extend ampl::DataFrame{


void setValueSWIG(ampl::Tuple rowIndex, fmt::CStringRef colHeader, ampl::Variant value)
{
	self->setValue(ampl::TupleRef(rowIndex), colHeader, value);
}
void setValueSWIG(std::size_t rowIndex, std::size_t colIndex, ampl::Variant value)
{
	self->setValue(rowIndex, colIndex, value);
}
void addColumnSWIG(fmt::CStringRef header)
{
  return self->addColumn(header);
}
void addColumnSWIG(fmt::CStringRef header, const char* args[])
{
  return self->addColumn(header, ampl::internal::Args(args));
}
void addColumnSWIG(fmt::CStringRef header, double* args)
{
  return self->addColumn(header, ampl::internal::Args(args));
}
  void addRow(ampl::Tuple tuple)
  {
  return self->addRow(ampl::TupleRef(tuple));
  }
  ampl::internal::Slice<true> getRow(ampl::Tuple tuple)
  {
  return self->getRow(ampl::TupleRef(tuple));
  }
  void setColumnSWIG(fmt::CStringRef header, const char* args[], std::size_t n)
  {
    self->setColumn(header, ampl::internal::Args(args), n);
  }
  void setColumnSWIG(fmt::CStringRef header, double *values, std::size_t n)
  {
    self->setColumn(header, ampl::internal::Args(values), n);
  }
  void setArraySWIG(double* args, double* values,  std::size_t n)
  {
    self->setArray(n, ampl::internal::Args(args), values);
  }
  void setArraySWIG(const char* args[], double* values,  std::size_t n)
  {
    self->setArray(n, ampl::internal::Args(args), values);
  }
  void setArraySWIG(double* args, const char* const *values,  std::size_t n)
  {
    self->setArray(n, ampl::internal::Args(args), values);
  }
  void setArraySWIG(const char* args[], const char* const *values,  std::size_t n)
  {
    self->setArray(n, ampl::internal::Args(args), values);
  }
  void setMatrixSWIG(double* row_indices, std::size_t rown, double* col_indices, std::size_t coln,
    const double* values)
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), values);
  }
  void setMatrixSWIG(const char* row_indices[], std::size_t rown, const char* col_indices[], std::size_t coln,
    const double* values)
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), values);
  }
  void setMatrixSWIG(double* row_indices, std::size_t rown, const char*col_indices[], std::size_t coln,
    const double* values)
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), values);
  }
  void setMatrixSWIG(const char* row_indices[], std::size_t rown, double* col_indices, std::size_t coln,
    const double* values)
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), values);
  }

  void setMatrixSWIG(double* row_indices, std::size_t rown, double* col_indices, std::size_t coln,
    const char* args[])
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), args);
  }
 
  void setMatrixSWIG(double* row_indices, std::size_t rown, const char* col_indices[], std::size_t coln,
    const char* args[])
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), args);
  }
  void setMatrixSWIG(const char* row_indices[], std::size_t rown, double* col_indices, std::size_t coln,
    const char* args[])
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), args);
  }
  void setMatrixSWIG(const char* row_indices[], std::size_t rown, const char* col_indices[], std::size_t coln,
    const char* args[])
  {
    self->setMatrix(rown, ampl::internal::Args(row_indices), coln,
      ampl::internal::Args(col_indices), args);
  }
  static DataFrame factory(int numberOfIndexColumns, const char* args[], int count)
  {
    ampl::StringArgs s(args, count);
    return ampl::DataFrame(numberOfIndexColumns, s);
  }
}
%template(DataFrameColumn)ampl::internal::Slice<false>;
%template(DataFrameRow)ampl::internal::Slice<true>;