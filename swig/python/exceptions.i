%include "exception.i"
%exception{
  try {
  $action
}
catch (std::range_error) {
  SWIG_exception(SWIG_ValueError, "Range Error");
}
catch (ampl::AMPLException e) {
  SWIG_exception(SWIG_RuntimeError, e.what());
}
catch (std::invalid_argument e) {
  SWIG_exception(SWIG_ValueError, e.what());
}
catch (std::logic_error e) {
  SWIG_exception(SWIG_TypeError, e.what());
}
catch (ampl::UnsupportedOperationException e)
{
	SWIG_exception(SWIG_TypeError, e.what());
}
catch (ampl::LicenseException e) {
	SWIG_exception(SWIG_SystemError, e.what());
}
catch (ampl::FileIOException e) {
	SWIG_exception(SWIG_IOError, e.what());
}
catch (std::runtime_error e) {
  SWIG_exception(SWIG_RuntimeError, e.what());
}
catch (std::exception e) {
  SWIG_exception(SWIG_UnknownError, e.what());
}
catch (...) {
  SWIG_exception(SWIG_UnknownError,"Unknown exception");
}
}
