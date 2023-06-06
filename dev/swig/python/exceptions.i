%include "exception.i"

%exceptionclass PresolveException;
%exceptionclass InfeasibilityException;

%extend ampl::PresolveException {
    const char* _str_() const {
            return $self->what();
    }
}

%extend ampl::InfeasibilityException {
    const char* _str_() const {
            return $self->what();
    }
}

%exception{
  try {
  $action
}
catch (std::range_error) {
  SWIG_exception(SWIG_ValueError, "Range Error");
}
catch (const ampl::AMPLException &e) {
  SWIG_exception(SWIG_RuntimeError, e.what());
}
catch (const ampl::PresolveException &e) {
  ampl::PresolveException *ecopy = new ampl::PresolveException(e);
  PyObject *err = SWIG_NewPointerObj(ecopy, SWIGTYPE_p_ampl__PresolveException, 1);
  PyErr_SetObject(SWIG_Python_ExceptionType(SWIGTYPE_p_ampl__PresolveException), err);
  SWIG_fail;
}
catch (const ampl::InfeasibilityException &e) {
  ampl::InfeasibilityException *ecopy = new ampl::InfeasibilityException(e);
  PyObject *err = SWIG_NewPointerObj(ecopy, SWIGTYPE_p_ampl__InfeasibilityException, 1);
  PyErr_SetObject(SWIG_Python_ExceptionType(SWIGTYPE_p_ampl__InfeasibilityException), err);
  SWIG_fail;
}
catch (const std::invalid_argument &e) {
  SWIG_exception(SWIG_ValueError, e.what());
}
catch (const std::out_of_range &e) {
  // SWIG_KeyError does not exist
  SWIG_Python_SetErrorMsg(PyExc_KeyError, e.what()); SWIG_fail;
}
catch (const std::logic_error &e) {
  SWIG_exception(SWIG_TypeError, e.what());
}
catch (const ampl::UnsupportedOperationException &e)
{
	SWIG_exception(SWIG_TypeError, e.what());
}
catch (const ampl::LicenseException &e) {
	SWIG_exception(SWIG_SystemError, e.what());
}
catch (const ampl::FileIOException &e) {
	SWIG_exception(SWIG_IOError, e.what());
}
catch (const std::runtime_error &e) {
  SWIG_exception(SWIG_RuntimeError, e.what());
}
catch (const std::exception &e) {
  SWIG_exception(SWIG_UnknownError, e.what());
}
catch (...) {
  SWIG_exception(SWIG_UnknownError,"Unknown exception");
}
}
