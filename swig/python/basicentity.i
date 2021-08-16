namespace ampl {
  namespace internal{
    template <class InstanceClass> class EntityWrapper {
    public:
      typedef std::pair<ampl::TupleRef, InstanceClass> ValueType;
      typedef  InstanceClass InstanceType;
	  typedef ampl::TupleRef KeyType;
    };
    template <class FunctionClass> 
    class CountedIterator
    {
    public:
      bool operator==(const CountedIterator &other) const;

      bool operator!=(const CountedIterator &other) const;
    //  typename FunctionClass::ValueType operator*() const;
      

      CountedIterator &operator=(const CountedIterator &other);
      CountedIterator &operator++();
      CountedIterator operator++(int);
      %extend{
        typename FunctionClass::KeyType  first()
      {
        return self->operator*().first;
        }
      typename FunctionClass::InstanceType  second()
      {
        return self->operator*().second;
      }
      }

    };
  }
}