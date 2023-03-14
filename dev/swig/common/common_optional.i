%rename(hasValue) ampl::Optional::operator bool;
%ignore ampl::Optional::operator->;
%ignore ampl::Optional::operator*;
%include "ampl/optional.h"
%template(OptionalInt)ampl::Optional<int>;
%template(OptionalString)ampl::Optional<std::string>;
%template(OptionalBool)ampl::Optional<bool>;
%template(OptionalDouble)ampl::Optional<double>;