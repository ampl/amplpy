// Standard things
%include "std_string.i"


%feature("valuewrapper") std::pair<const char*, const char*>;
%ignore std::pair<const char*, const char*>::pair(); 
%include <std_pair.i>


%rename(Clone) *::operator=; 



// Include all things
%{
	#include "ampl/environment.h"
%}

namespace ampl
{
  namespace internal{
    class EnvironmentIterator {
    public:
    typedef  std::pair<const char*, const char*> ValueType;
	  typedef const char* KeyType;
	  typedef const char* InstanceType;
    };
  }
}
	
%include "ampl/environment.h"

%template(EnvironmentIteratorTemplate) ampl::internal::CountedIterator<ampl::internal::EnvironmentIterator>;


