%typemap(in, canthrow = 1) fmt::CStringRef
%{
  $1 = PyUnicode_AsUTF8($input);
%}
// Copy the typecheck code for "char *".
%typemap(typecheck) fmt::CStringRef = char *;
