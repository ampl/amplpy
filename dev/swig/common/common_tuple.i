// Tuples
namespace ampl
{
class TupleRef
{
  TupleRef(ampl::TupleRef t);
  public:
  TupleRef(ampl::Tuple t);
  std::size_t size();
  std::string toString();
  Variant operator[](int index);
};
class Tuple
{
public:
  Tuple();
  Tuple(double d);
  Tuple(const char *s);
  std::size_t size();
  std::string toString();
  Variant operator[](int index);


%extend {

  bool operator==(ampl::Tuple &other)
  {
  return (other == *self);
  } 
  static ampl::Tuple Factory(VariantArray &args, std::size_t count) 
  {
    return ampl::Tuple(VariantArray_cast(&args), count);
  }
  static ampl::Tuple Factory(ampl::TupleRef t)
  {
    return ampl::Tuple(t);
  }
}
};
} // ampl