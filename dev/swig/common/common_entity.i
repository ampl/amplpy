// For EntityArgs
%array_class(ampl::Entity, EntityArray);

namespace ampl{

  class Entity
	{
		public:
    std::string toString();
		std::string name();
		std::string type();
		int indexarity();
		bool isScalar();
		int numInstances();
    ampl::StringArray getIndexingSets() const;
    ampl::StringArray xref() const;

		ampl::DataFrame getValues();
	//	ampl::DataFrame getValues(StringArgs args);
    void setValues(ampl::DataFrame data);
    %extend
    {
      // The following to avoid the ugly StringArgs
    ampl::DataFrame getValues(const char* args[], int count)
    {
      ampl::StringArgs s(args, count);
      return self->getValues(s);
    }
    }
	};

  template <class InstanceClass> class BasicEntity : public Entity
  {
  public:
   typedef internal::CountedIterator<internal::EntityWrapper<InstanceClass> > iterator;
   %newobject BasicEntity::begin;
   %newobject BasicEntity::end;
   %newobject BasicEntity::find;
   iterator begin();
   iterator end();
   iterator find(Tuple t);

   	InstanceClass get();
		InstanceClass get(ampl::Tuple index);
  };

  class EntityArgs
  {
  public:
  %extend{
  static ampl::EntityArgs Factory(EntityArray &args, std::size_t count)
  {
    return ampl::EntityArgs(EntityArray_cast(&args), count);
  }
  }
  };
} // ampl


%template(BasicEntityVariable) ampl::BasicEntity< ampl::VariableInstance >;
%template(BasicEntityConstraint) ampl::BasicEntity< ampl::ConstraintInstance >;
%template(BasicEntitySet) ampl::BasicEntity< ampl::SetInstance >;
%template(BasicEntityObjective) ampl::BasicEntity< ampl::ObjectiveInstance >;
%template(BasicEntityParameter) ampl::BasicEntity< ampl::VariantRef >;
%template(BasicEntityTable) ampl::BasicEntity< ampl::TableInstance >;

namespace ampl
{
	class Constraint : public ampl::BasicEntity<ampl::ConstraintInstance>
	{
		public:
		bool isLogical();
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
	namespace var {

	enum Integrality {
	  CONTINUOUS,
	  BINARY,
	  INTEGER
	};
	}

	class Variable  : public ampl::BasicEntity<ampl::VariableInstance>
	{
		public:
		var::Integrality integrality();
		void fix();
		void fix(double value);
		void unfix();
		void setValue(double value);
		double value();
		std::string astatus();
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
		std::string sstatus();
		std::string status();
	};
	class Objective  :  public ampl::BasicEntity<ampl::ObjectiveInstance>
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

  class Set  : public ampl::BasicEntity<ampl::SetInstance>
	{
		public:
      std::size_t arity() const;
      DataFrame getValues() const;
      std::size_t size() const;
      ampl::SetInstance::MemberRange members() const;

      void setValues(ampl::DataFrame data);
      %extend{
      bool contains(ampl::Tuple t) const
      {
        return self->contains(ampl::TupleRef(t));
      }
      void setValuesTuples(const ampl::Tuple *t, std::size_t n)
      {
        return self->setValues(t, n);
      }
      void setValues(TupleArray &t, std::size_t n)
      {
        return self->setValues(TupleArray_cast(&t), n);
      }
      void setValuesDbl(double *values, std::size_t n)
      {
        return self->setValues(ampl::internal::Args(values), n);
      }
      void setValuesStr(const char* args[], std::size_t n)
      {
        return self->setValues(ampl::internal::Args(args), n);
      }
      }
	};
  class Table : public ampl::BasicEntity<ampl::TableInstance>
	{

  };
  class Parameter : public ampl::BasicEntity<ampl::VariantRef>
	{
		public:
		bool isSymbolic();
    bool hasDefault();
    %extend{
      void set(ampl::Variant value)
    {
      self->set(ampl::VariantRef(value));
    }
      void set(double value)
      {
        self->set(ampl::VariantRef(value));
      }
    void set(const char* value)
    {
      self->set(ampl::VariantRef(value));
    }

      void set(ampl::Tuple index, ampl::Variant value)
    {
      self->set(ampl::TupleRef(index), ampl::VariantRef(value));
    }
      void set(ampl::Tuple index, double value)
      {
        self->set(ampl::TupleRef(index), ampl::VariantRef(value));
      }
    void set(ampl::Tuple index, const char* value)
    {
      self->set(ampl::TupleRef(index), ampl::VariantRef(value));
    }
    void setValues(const ampl::Tuple *indices, const double* values, std::size_t nvalues)
      {
        self->setValues(indices, ampl::internal::Args(values), nvalues);
      }
      void setValues(TupleArray &indices, double* values, std::size_t nvalues)
      {
        self->setValues(TupleArray_cast(&indices), ampl::internal::Args(values), nvalues);
      }
      void setValues(const ampl::Tuple *indices, const char* args[], std::size_t nvalues)
      {
        self->setValues(indices, ampl::internal::Args(args), nvalues);
      }
      void setValues(TupleArray &indices, const char* args[], std::size_t nvalues)
      {
        self->setValues(TupleArray_cast(&indices), ampl::internal::Args(args), nvalues);
      }


      void setValues(double* values, std::size_t n)
      {
        self->setValues(ampl::internal::Args(values), n);
      }
      void setValues(const char* args[], std::size_t n)
      {
        self->setValues(ampl::internal::Args(args), n);
      }
      void setValues(std::size_t num_rows, const char* row_indices[],
        std::size_t num_cols, const char* col_indices[],
        const double* values, bool transpose)
      {
        self->setValues(num_rows, ampl::internal::Args(row_indices),
          num_cols,ampl::internal::Args(col_indices), values, transpose);
      }
      void setValues(std::size_t num_rows, double* row_indices,
        std::size_t num_cols, double* col_indices,
        const double* values, bool transpose)
      {
        self->setValues(num_rows, ampl::internal::Args(row_indices),
          num_cols,ampl::internal::Args(col_indices), values, transpose);
      }
    }






	};
}
%template(VariableIteratorWrapper) ampl::internal::EntityWrapper<ampl::VariableInstance> ;
%template(VariableIterator) ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::VariableInstance> >;
%template(ConstraintIteratorWrapper) ampl::internal::EntityWrapper<ampl::ConstraintInstance> ;
%template(ConstraintIterator) ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::ConstraintInstance> >;
%template(ObjectiveIteratorWrapper) ampl::internal::EntityWrapper<ampl::ObjectiveInstance> ;
%template(ObjectiveIterator) ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::ObjectiveInstance> >;
%template(SetIteratorWrapper) ampl::internal::EntityWrapper<ampl::SetInstance> ;
%template(SetIterator) ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::SetInstance> >;
%template(TableIteratorWrapper) ampl::internal::EntityWrapper<ampl::TableInstance> ;
%template(TableIterator) ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::TableInstance> >;

%template(ParameterIteratorWrapper)ampl::internal::EntityWrapper<ampl::VariantRef>;
%template(ParameterIterator)ampl::internal::CountedIterator<ampl::internal::EntityWrapper<ampl::VariantRef> >;
