%include "exception.i"

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
catch (const ampl::InfeasibilityException &e) {
  std::string msg = "InfeasibilityException: " + std::string(e.what());
  SWIG_exception(SWIG_RuntimeError, msg.c_str());
}
catch (const ampl::PresolveException &e) {
  std::string msg = "PresolveException: " + std::string(e.what());
  SWIG_exception(SWIG_RuntimeError, msg.c_str());
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
catch (const ampl::UnsupportedOperationException &e) {
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
