namespace ampl {
  enum Type {
    /**
    Empty variant, i.e. one that does not hold a value
    */
    EMPTY,
    /**
    Numeric (floating point) value
    */
    NUMERIC,
    /**
    String value
    */
    STRING
  };
  class Variant
  {
  public:
    Variant(std::string s);
    Variant(double d);
    Variant(const ampl::VariantRef& other);
    std::string str() const;
    double dbl() const;
    Type type() const;
    std::string toString();
    %extend{
     bool equals(Variant &b)
    {
      return ampl::internal::compare(*$self, b)==0;
    }
    int compare(Variant &b)
    {
      return ampl::internal::compare(*$self, b);
    }
    }
  };

  class VariantRef
  {
  public:
    VariantRef(std::string s);
    VariantRef(double d);
    VariantRef(const ampl::Variant& other);
    std::string str() const;
    double dbl() const;
    Type type() const; 
    std::string toString();
    %extend{
    bool equals(VariantRef &b)
    {
      return ampl::internal::compare(*$self, b) == 0;
    }
    int compare(VariantRef &b)
    {
      return ampl::internal::compare(*$self, b);
    }
    }
  };
}