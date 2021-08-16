%module(directors = "1")  amplpython
%feature("flatnested");

// Add the following for windows, otherwise it tries to link
// to python debug libraries (not always available)
%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}

%{
#if PY_VERSION_HEX>=0x03000000
  #define _PyString_AsString(str) PyUnicode_AsUTF8(str)
  #define _PyString_Check(obj) PyUnicode_Check(obj)
#else
  #define _PyString_AsString(str) PyString_AsString(str)
  #define _PyString_Check(obj) PyString_Check(obj)
#endif
%}

// ********* Common declarations *********
%include "../common/common.i"

// ************* Exception handling *************
%include "std_except.i" // Fix: Warning 401: Nothing known about base class 'std::runtime_error'.
%include "exceptions.i"

// Basic types
%include "cstringref.i"
// Enable arrays of base types
%include "carrays.i"
%include "stringarrays.i"
%include "doublearrays.i"
%apply char ** { const char* args[] }

// Enable arrays of AMPL types
%array_class(ampl::Variant, VariantArray);
%array_class(ampl::Tuple, TupleArray);

// Optional
%include "../common/common_optional.i"

// Variant code
%include "../common/common_variant.i"

// Tuples
%include "../common/common_tuple.i"

// Rename overloaded methods
%include "rename.i"

// DataFrame
// The following renames methods which are not supported by
// Python
%include "../common/common_dataframe.i"

// Instance classes
%include "../common/common_instance.i"

// Entities and EntityArgs
%include "basicentity.i"
%include "../common/common_entity.i"

// EntityMap
%rename(RowIterator) ampl::internal::Slice<true>::iterator;
%rename(EntityMapVariableIterator)ampl::EntityMap<ampl::Variable>::iterator;
%rename(EntityMapConstraintIterator)ampl::EntityMap<ampl::Constraint>::iterator;
%rename(EntityMapObjectiveIterator)ampl::EntityMap<ampl::Objective>::iterator;
%rename(EntityMapSetIterator)ampl::EntityMap<ampl::Set>::iterator;
%rename(EntityMapParameterIterator)ampl::EntityMap<ampl::Parameter>::iterator;
%rename(EntityMapTableIterator)ampl::EntityMap<ampl::Table>::iterator;
%include "../common/common_entitymap.i"

// AMPL Exception
%include "ampl/amplexception.h"
// Output and error handlers
%newobject ampl::ErrorHandler::warning(const ampl::AMPLException&);
%newobject ampl::ErrorHandler::error(const ampl::AMPLException&);
%feature("director") ampl::ErrorHandler;
%feature("director") ampl::OutputHandler;
%feature("director") ampl::Runnable;
%clearnodefaultctor; // needed for handlers
%include "ampl/errorhandler.h"
%include "ampl/runnable.h"
// %ignore ampl::output::Kind; // swig does not keep the namespace
%include "ampl/output.h"

// Environment
%include "../common/common_environment.i"

// AMPL
%ignore ampl::AMPL::getData(StringArgs statements) const;
%ignore ampl::AMPL::display(StringArgs amplExpressions);
%include "ampl/ampl.h"
%extend ampl::AMPL{
  // The following to avoid the ugly StringArgs and
  void display(const char* args[], int count)
{
  ampl::StringArgs s(args, count);
  self->display(s);
}
ampl::DataFrame getData(const char* args[], int count)
{
  ampl::StringArgs s(args, count);
  return self->getData(s);
}
}

%include "extensions.i"
