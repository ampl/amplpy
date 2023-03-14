%feature("valuewrapper") ampl::EntityMap<ampl::Variable>;
%feature("valuewrapper") ampl::EntityMap<ampl::Constraint>;
%feature("valuewrapper") ampl::EntityMap<ampl::Objective>;
%feature("valuewrapper") ampl::EntityMap<ampl::Set>;
%feature("valuewrapper") ampl::EntityMap<ampl::Table>;
%feature("valuewrapper") ampl::EntityMap<ampl::Parameter>;

namespace ampl
{
  template <class EntityClass> class EntityMap {
  public:
    class iterator
    {
    public:
      bool operator==(const iterator& other) const;
      bool operator!=(const iterator& other) const;
      EntityClass operator*();
      iterator& operator=(const iterator& other);
      iterator& operator++();
      iterator operator++(int);
    };
    iterator begin()const;
    iterator end()const;
    iterator find(char* name);
    std::size_t size()const;
    EntityClass operator[](fmt::CStringRef name)const;
  };
}

%template(EntityMapVariable)ampl::EntityMap<ampl::Variable>;
%template(EntityMapConstraint)ampl::EntityMap<ampl::Constraint>;
%template(EntityMapObjective)ampl::EntityMap<ampl::Objective>;
%template(EntityMapSet)ampl::EntityMap<ampl::Set>;
%template(EntityMapTable)ampl::EntityMap<ampl::Table>;
%template(EntityMapParameter)ampl::EntityMap<ampl::Parameter>;
