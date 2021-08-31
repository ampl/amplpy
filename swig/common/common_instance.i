%feature("valuewrapper") ampl::SetInstance::MemberRange::iterator;
%feature("valuewrapper") ampl::SetInstance::MemberRange;
namespace ampl {
class Entity;
class Instance
{
  public:

  std::string toString()const;
  std::string name() const;
  ampl::Entity entity() const;
  ampl::Tuple key() const;
};

class SetInstance : public ampl::Instance
{
public:
  std::size_t size() const;
  bool contains(TupleRef t) const;
  ampl::DataFrame getValues() const;
  void setValues(ampl::DataFrame data);

  class MemberRange {
  public:
    explicit MemberRange(internal::SetInstance* impl_);
    class iterator {
    public:
      TupleRef operator*() const { return TupleRef(*ptr_); }
      iterator& operator++();
      iterator operator++(int);
      bool operator==(const iterator& other) const;
      bool operator!=(const iterator& other) const;
    };
    iterator begin() const;
    iterator end() const;
  };
  MemberRange members() const;

  %extend{
    bool Contains(ampl::Tuple t) const
  {
    return self->contains(ampl::TupleRef(t));
  }
  void setValues(const ampl::Tuple *t, std::size_t n)
  {
    return self->setValues(t, n);
  }
  void setValues(TupleArray &t, std::size_t n)

  {
    return self->setValues(TupleArray_cast(&t), n);
  }
  void setValues(double *values, std::size_t n)
  {
    return self->setValues(ampl::internal::Args(values), n);
  }
  void setValues(const char *args[], std::size_t n)
  {
    return self->setValues(ampl::internal::Args(args), n);
  }
  }
};

class ObjectiveInstance : public ampl::Instance
{
public:
  double value();
	std::string  astatus();
	std::string  sstatus();
	int exitcode();
	std::string message();
	std::string  result();
	void drop();
	void restore();
	bool minimization();
};

class VariableInstance : public ampl::Instance
{
public:
  void fix();
	void fix(double value);
	void unfix();
	void setValue(double value);
	double value();

	int defeqn();
	double dual();
	double init();
	double init0();
	double lb();
	double ub();
	double lb0();
	double ub0();
	double lb1();
	double ub1();
	double lb2();
	double ub2();
	double lrc();
	double urc();
	double lslack();
	double uslack();
	double rc();
	double slack();
  std::string astatus();
	std::string sstatus();
	std::string status();
};

class ConstraintInstance : public ampl::Instance
{
public:
	void drop();
	void restore();
	double body();
	std::string astatus();
	int defvar();
	double dinit() ;
	double dinit0() ;
	double dual() ;
	double lb() ;
	double ub() ;
	double lbs() ;
	double ubs() ;
	double ldual() ;
	double udual() ;
	double lslack() ;
	double uslack() ;
	double slack() ;
	std::string sstatus();
	std::string status();
	void setDual(double dual) ;
	double val();
};

class TableInstance : public ampl::Instance
{
};

}// ampl
