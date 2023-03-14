%typemap(in, canthrow = 1) fmt::CStringRef
%{
  $1 = _PyString_AsString($input);
%}
// Copy the typecheck code for "char *".
%typemap(typecheck) fmt::CStringRef = char *;
