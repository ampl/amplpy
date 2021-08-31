%rename(RowIterator) ampl::internal::Slice<true>::iterator;
%rename(ColIterator) ampl::internal::Slice<false>::iterator;

%rename(getRowTpl) ampl::DataFrame::getRow(ampl::Tuple);

%rename(addColumn) ampl::DataFrame::addColumnSWIG(fmt::CStringRef);
%rename(addColumnDbl) ampl::DataFrame::addColumnSWIG(fmt::CStringRef, double*);
%rename(addColumnStr) ampl::DataFrame::addColumnSWIG(fmt::CStringRef, const char*[]);

%rename(setColumnDbl) ampl::DataFrame::setColumnSWIG(fmt::CStringRef, double*, std::size_t);
%rename(setColumnStr) ampl::DataFrame::setColumnSWIG(fmt::CStringRef, const char*[], std::size_t);

%rename(setArrayDblDbl) ampl::DataFrame::setArraySWIG(double* , double* , std::size_t );
%rename(setArrayStrDbl) ampl::DataFrame::setArraySWIG(const char* args[], double*, std::size_t);
%rename(setArrayDblStr) ampl::DataFrame::setArraySWIG(double* , const char* const *, std::size_t);
%rename(setArrayStrStr) ampl::DataFrame::setArraySWIG(const char*[], const char* const *, std::size_t);

%rename(setMatrixDblDblDbl) ampl::DataFrame::setMatrixSWIG(double*, std::size_t, double*, std::size_t, const double*);
%rename(setMatrixDblStrDbl) ampl::DataFrame::setMatrixSWIG(double*, std::size_t, const char*[], std::size_t, const double*);
%rename(setMatrixStrDblDbl) ampl::DataFrame::setMatrixSWIG(const char*[], std::size_t, double*, std::size_t, const double*);
%rename(setMatrixStrStrDbl) ampl::DataFrame::setMatrixSWIG(const char* [], std::size_t, const char*[], std::size_t, const double*);

%rename(setMatrixDblDblStr) ampl::DataFrame::setMatrixSWIG(double*, std::size_t, double*, std::size_t, const char*[]);
%rename(setMatrixDblStrStr) ampl::DataFrame::setMatrixSWIG(double*, std::size_t, const char*[], std::size_t, const char*[]);
%rename(setMatrixStrDblStr) ampl::DataFrame::setMatrixSWIG(const char*[], std::size_t, double*, std::size_t, const char*[]);
%rename(setMatrixStrStrStr) ampl::DataFrame::setMatrixSWIG(const char*[], std::size_t, const char*[], std::size_t, const char*[]);

%rename(setValuesTaDbl) ampl::Parameter::setValues(const ampl::Tuple *indices, const double *values, std::size_t nvalues);
%rename(setValuesTaStr) ampl::Parameter::setValues(const ampl::Tuple *indices, const char* args[], std::size_t nvalues);
%rename(setValuesTupleArrayDbl) ampl::Parameter::setValues(TupleArray &indices, double* values, std::size_t nvalues);
%rename(setValuesTupleArrayStr) ampl::Parameter::setValues(TupleArray &indices, const char* args[], std::size_t nvalues);
%rename(setValuesDbl) ampl::Parameter::setValues(double* values, std::size_t n);
%rename(setValuesStr) ampl::Parameter::setValues(const char* args[], std::size_t n);
%rename(setValuesDbl) ampl::Set::setValues(double *,std::size_t);
%rename(setValuesStr) ampl::Set::setValues(char const *[],std::size_t);

%rename(setValuesTuples) ampl::SetInstance::setValues(const ampl::Tuple *indices, std::size_t nvalues);
%rename(setValuesDbl) ampl::SetInstance::setValues(double *,std::size_t);
%rename(setValuesStr) ampl::SetInstance::setValues(char const *[],std::size_t);
%rename(setValuesDf) ampl::SetInstance::setValues(ampl::DataFrame);

%rename(setTplDbl) ampl::Parameter::set(ampl::Tuple,double);
%rename(setTplStr) ampl::Parameter::set(ampl::Tuple,char const *);

%rename(setValuesDf) ampl::Entity::setValues(ampl::DataFrame);
%rename(getValuesLst) ampl::Entity::getValues(char const *[],int);

%rename(displayLst)    ampl::AMPL::display(char const *[],int);
