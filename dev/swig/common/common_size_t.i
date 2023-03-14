// std::size_t
%inline %{
  namespace std {
#if _WIN64
    typedef unsigned __int64 size_t;
#elif __clang__
    //
#elif __amd64__
    typedef unsigned long size_t;
#else
    typedef unsigned int size_t;
#endif
 }
%}