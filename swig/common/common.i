%nodefaultctor;

// Always use explicit
#define FMT_HAS_FEATURE(arg) 1

#ifdef _WIN32
  %include <windows.i>
#endif

// Ignore default constructor for entity iterators
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::VariableInstance>;
%ignore std::pair<ampl::TupleRef, ampl::VariableInstance>::pair();
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::ConstraintInstance>;
%ignore std::pair<ampl::TupleRef, ampl::ConstraintInstance>::pair();
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::ObjectiveInstance>;
%ignore std::pair<ampl::TupleRef, ampl::ObjectiveInstance>::pair();
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::SetInstance>;
%ignore std::pair<ampl::TupleRef, ampl::SetInstance>::pair();
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::TableInstance>;
%ignore std::pair<ampl::TupleRef, ampl::TableInstance>::pair();
%feature("valuewrapper") std::pair<ampl::TupleRef, ampl::Variant>;



// Include all things
%{
  #include "ampl/ampl.h"
%}

// Standard things
%include "std_string.i"
%include "carrays.i"
%include "exception.i"

// Everything is returned by value really
%feature("valuewrapper") ampl::Variant;
%feature("valuewrapper") ampl::VariantRef;
%feature("valuewrapper") ampl::EntityArgs;
%feature("valuewrapper") ampl::Parameter;
%feature("valuewrapper") ampl::Set;
%feature("valuewrapper") ampl::Variable;
%feature("valuewrapper") ampl::Objective;
%feature("valuewrapper") ampl::Constraint;
%feature("valuewrapper") ampl::Table;
%feature("valuewrapper") ampl::Entity;
%feature("valuewrapper") ampl::Instance;
%feature("valuewrapper") ampl::ParameterInstance;
%feature("valuewrapper") ampl::SetInstance;
%feature("valuewrapper") ampl::SetInstance::MemberRange;
%feature("valuewrapper") ampl::VariableInstance;
%feature("valuewrapper") ampl::ObjectiveInstance;
%feature("valuewrapper") ampl::ConstraintInstance;
%feature("valuewrapper") ampl::TableInstance;
%feature("valuewrapper") ampl::internal::Slice<false>;
%feature("valuewrapper") ampl::internal::Slice<true>;
%feature("valuewrapper") ampl::internal::Slice<true>::iterator;
%feature("valuewrapper") ampl::internal::Slice<false>::iterator;

// Rename all operators, when provided
%rename(getIndex) *::operator[];
%rename(clone) *::operator=;
%rename(equals) *::operator==;
%rename(differs) *::operator!=;
%rename(less) *::operator<;
%rename(lessorequals) *::operator<=;
%rename(greater) *::operator>;
%rename(greaterorequals) *::operator>=;
%rename(dereference) *::operator*;
%rename(postIncrement) *::operator++;
%rename(postIncrementBy) *::operator++(int);

namespace ampl
{
  class StringArray
  {
  public:
    std::size_t size() const;
    const char* operator[](std::size_t index) const;
  };
  class StringRefArray
  {
  public:
    std::size_t size() const;
    const char* operator[](std::size_t index) const;
  };
}

namespace std
{
class runtime_error
{
public:
	const char* what() const;
};
}
