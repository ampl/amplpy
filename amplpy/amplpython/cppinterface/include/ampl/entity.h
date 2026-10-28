#ifndef AMPL_ENTITY_H
#define AMPL_ENTITY_H

#include <iterator>
#include <map>
#include <string>
#include <vector>

#include "ampl/ampl_c.h"
#include "ampl/cstringref.h"
#include "ampl/arg.h"
#include "ampl/declarations.h"
#include "ampl/macros.h"
#include "ampl/instance.h"
#include "ampl/string.h"
#include "ampl/tuple.h"
#include "ampl/variant.h"

#include <iostream>

namespace ampl {

// Forward declaration
class DataFrame;
template <class EntityClass>
class EntityMap;


template<typename T>
struct is_parameter_instance : std::false_type {};

template<>
struct is_parameter_instance<Variant> : std::true_type {};

/**
 * An %AMPL entity such as a parameter or a variable.
 *
 * An entity can either represent a single instance of an %AMPL algebraic entity
 * or, if the corresponding declaration has an indexing expression, a mapping
 * from keys to instances. In the derived classes, it has methods to access
 * instance-level properties which can be used in case the represented entity is
 * scalar.
 * <p>
 * To gain access to all the values in an entity (for all instances and all
 * suffixes for that entities), use the function Entity::getValues().
 * <p>
 * The algebraic entities which currenty have an equivalent class in the API
 * are: <ul> <li> Variables (see ampl::Variable)</li> <li> Constraints (see
 * ampl::Constraint)</li> <li> Objectives (see ampl::Objective)</li> <li> Sets
 * (see ampl::Set)</li> <li> Parameters (see ampl::Parameter)</li>
 * </ul>
 */
class Entity {
 public:
  /**
   * Get the name of this entity
   */
  std::string name() const { return name_; }

  /**
   * Get the type of this entity
   */
  std::string type() const {
    const char *typestr;
    AMPL_CALL_CPP(AMPL_EntityGetTypeString(ampl_, name_.c_str(), &typestr));
    return typestr;
  }

  /**
   * Get expand message of this entity
   */
  std::string expand() const {
    char *expand;
    AMPL_CALL_CPP(AMPL_EntityExpand(ampl_, name_.c_str(), &expand));
    std::string result(expand);
    AMPL_StringFree(&expand);
    return result;
  }

  /**
  * Get the indexarity of this entity (sum of the dimensions of the indexing
  * sets).
  * This value indicates the arity of the Tuple to be passed to the method
  * BasicEntity::get() in order to access an instance of this entity.
  * See the following %AMPL examples
  * \rststar
  *
  * .. code-block:: ampl
  *
  *       var x;               # indexarity = 0
  *       var y {1..2};        # indexarity = 1
  *       var z {1..2,3..4};   # indexarity = 2
  *       var zz {{(1, 2)}};   # indexarity = 2
  *
  * \endrststar
  * \return The sum of the dimensions of the indexing sets or 0 if the
  entity is not indexed
  */
  std::size_t indexarity() const {
    size_t indexarity;
    AMPL_CALL_CPP(AMPL_EntityGetIndexarity(ampl_, name_.c_str(), &indexarity));
    return indexarity;
  }

  /**
   * Check whether this entity is scalar. Equivalent to testing whether
   * indexarity() is equal to zero.
   * \return True if the entity is scalar (not indexed over any set)
   */
  bool isScalar() const {
    size_t indexarity;
    AMPL_CALL_CPP(AMPL_EntityGetIndexarity(ampl_, name_.c_str(), &indexarity));
    return (indexarity == 0);
  }

  /**
   * Get the number of instances in this entity
   */
  std::size_t numInstances() const {
    size_t numInstances;
    AMPL_CALL_CPP(AMPL_EntityGetNumInstances(ampl_, name_.c_str(),
                               &numInstances));
    return numInstances;
  }

  /**
   * Get the %AMPL string representation of the sets on which this entity is
   * indexed. The obtained vector can be modified without any effect to the
   * entity.
   *
   * \return The string representation of the indexing sets for this entity or
   *         an empty array if the entity is scalar
   */
  StringArray getIndexingSets() const {
    size_t n;
    char **indexingsets;
    AMPL_CALL_CPP(AMPL_EntityGetIndexingSets(ampl_, name_.c_str(), &indexingsets, &n));
    ampl::StringArray strings((const char**)indexingsets, n);
    for (size_t i = 0; i < n; i++) AMPL_StringFree(&indexingsets[i]);
    free(indexingsets);
    return strings;
  }

  /**
   * Get the names of all entities which depend on this one.
   *
   * \return An array with the names of all entities which depend on this one.
   */
  StringArray xref() const {
    size_t n;
    char **xref;
    AMPL_CALL_CPP(AMPL_EntityGetXref(ampl_, name_.c_str(), &xref, &n));
    ampl::StringArray strings((const char**)xref, n);
    for (size_t i = 0; i < n; i++) AMPL_StringFree(&xref[i]);
    free(xref);
    return strings;
  }

  /**
  \rst
  Get the principal values of this entity as a DataFrame. The specific returned
  value depends on the
  type of entity (see list below).

  For:
   * Variables and Objectives it returns the suffix ``val``
   * Parameters it returns their values
   * Constraints it returns the suffix ``dual``
   * Sets it returns all the  of the set. Note that it does not
   * apply to indexed sets. See SetInstance::getValues
  \endrst
  * \return A DataFrame containing the values for all instances
  */
  DataFrame getValues() const;

  /**
  Get the specified suffixes value for all instances in a DataFrame
  \param suffixes Suffixes to get
  \return A DataFrame containing the specified values
  */
  DataFrame getValues(StringArgs suffixes) const;

  /**
   * Set suffix values for all instances of this entity from a DataFrame.
   *
   * The DataFrame must have index columns matching the entity's indexing sets
   * and one data column per suffix to set. Each data column name is used as
   * the suffix name. Not valid for parameters, sets, or tables.
   *
   * \param data A DataFrame containing the suffix values to assign.
   */
  void setSuffixes(DataFrame data);

  /**
   * Set a numeric suffix value for this scalar entity.
   *
   * Equivalent to the AMPL statement: ``let entityName.suffix := value;``
   * Not valid for parameters, sets, or tables.
   *
   * \param suffix Name of the suffix to set.
   * \param value  Numeric value to assign.
   */
  void setSuffix(std::string suffix, double value);

  /**
   * Set a string suffix value for this scalar entity.
   *
   * Equivalent to the AMPL statement: ``let entityName.suffix := value;``
   * Not valid for parameters, sets, or tables.
   *
   * \param suffix Name of the suffix to set.
   * \param value  String value to assign.
   */
  void setSuffix(std::string suffix, std::string value);

  /**
  \rst

  Set the values of this entiy to the correponding values of a
  DataFrame indexed over the same sets (or a subset).
  This function assigns the values in the first data column of
  the passed dataframe to the entity the function is called from.
  In particular, the statement:

  .. code-block:: c++

    x.setValues(y.getValues());

  is semantically equivalent to the AMPL statement:

  .. code-block:: ampl

    let {s in S} x[s] := y[s];

  \endrst
  \param data The data to set the entity to
  */
  void setValues(DataFrame data);

  /**
  Returns a string representation of this entity (its declaration)
  */
  std::string toString() const {
    char *declaration_c;
    AMPL_CALL_CPP(AMPL_EntityGetDeclaration(ampl_, name_.c_str(), &declaration_c));
    std::string declaration = declaration_c;
    AMPL_StringFree(&declaration_c);
    return declaration;
  }

  /**
   * Constructor to allow implicit conversion
   */
  template <class I>
  Entity(BasicEntity<I> other)
      : ampl_(other.ampl_), name_(other.name_), type_(other.type_) {}

  /**
   * Assignment operator
   */
  Entity &operator=(const Entity &rhs) {
    ampl_ = rhs.ampl_;
    name_ = rhs.name_;
    type_ = rhs.type_;
    return *this;
  }

  friend class AMPL;
  friend class DataFrame;
  friend class EntityArgs;
  friend class Instance;
  /**
   * Constructor to allow the construction of arrays of entities
   */
  Entity() {}

 protected:
  ::AMPL *ampl_;
  std::string name_;
  EntityType type_;
  explicit Entity(::AMPL *ampl, std::string name) : ampl_(ampl), name_(name) {
    AMPL_ENTITYTYPE type;
    AMPL_CALL_CPP(AMPL_EntityGetType(ampl, name.c_str(), &type));
    type_ = static_cast<EntityType>(type);
  }
};

/**
 * Infrastructure class to enable the inheriting classes type-safe access to
 * instances.
 */
template <class InstanceClass>
class BasicEntity : INHERITANCE Entity {
 public:
  using Entity::expand;
  using Entity::getIndexingSets;
  using Entity::getValues;
  using Entity::indexarity;
  using Entity::isScalar;
  using Entity::name;
  using Entity::numInstances;
  using Entity::setValues;
  using Entity::toString;
  using Entity::xref;
  using Entity::setSuffixes;

  /**
  Iterator for entities, represented by an iterator pointing to elements of type
  std::pair<Tuple, InstanceClass>
  */
  // typedef typename std::map<Tuple, InstanceClass>::iterator iterator;

  /** @name Instance access
   * Methods to access the instances which are part of this Entity
   */
  //@{
  /**
    * Get the instance corresponding to a scalar entity.
    *
    * \return The corresponding instance.
    * @throws runtime_error if the entity has been deleted in the underlying
    %AMPL interpreter
    * @throws logic_error if the entity is not scalar

    */
  InstanceClass get() const {
    if (!isScalar())
      throw ampl::UnsupportedOperationException("Not valid for not scalar entities.");
    return InstanceClass(ampl_, NULL, name_);
  }

  InstanceClass operator[](Tuple index) const { return get(index); }

  /**
   * Get the instance with the specified index
   *
   * \param index The tuple specifying the index
   * \return The corresponding instance
   * @throws out_of_range if an instance with the specified index does not exist
   * @throws out_of_range if the entity has been deleted in the underlying %AMPL
   * interpreter
   * @throws ampl::UnsupportedOperationException if the entity is scalar
   */
  InstanceClass get(Tuple index) const {
    AMPL_CALL_CPP(AMPL_EntityIsInstance(ampl_, name_.c_str(), index.impl()));
    if (!isScalar() || (index.size() == 1 && index[0].is_empty()))
      return InstanceClass(ampl_, index.impl(), name_);
    throw ampl::UnsupportedOperationException("Not valid for scalar entities.");
  }

  InstanceClass operator[](Variant v1) const { return get(v1); }

  /**
   * Get the instance with the specified index
   */
  InstanceClass get(Variant v1) const {
    Tuple t(v1);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   */
  InstanceClass get(Variant v1, Variant v2) const {
    Tuple t(v1, v2);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   */
  InstanceClass get(Variant v1, Variant v2, Variant v3) const {
    Tuple t(v1, v2, v3);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   *
   * \param v1 The Variant specifying the first element of the indexing tuple
   * \param v2 The Variant specifying the second element of the indexing
   * tuple \param v3 The Variant specifying the third element of the indexing
   * tuple \param v4 The Variant specifying the fourth element of the
   * indexing tuple \return The corresponding instance
   * @throws out_of_range if an instance with the specified index does not exist
   * @throws runtime_error if the entity has been deleted in the underlying
   * %AMPL interpreter
   * @throws ampl::UnsupportedOperationException if the entity is scalar
   */
  InstanceClass get(Variant v1, Variant v2, Variant v3, Variant v4) const {
    Tuple t(v1, v2, v3, v4);
    return get(t);
  }

  class iterator {
    public:

      iterator() : _it() {}
      explicit iterator(typename std::map<Tuple, InstanceClass>::iterator it) : _it(it) {}
      iterator& operator++() { ++_it; return *this; }
      iterator operator++(int) { iterator tmp = *this; ++_it; return tmp; }
      bool operator==(const iterator& other) const { return _it == other._it; }
      bool operator!=(const iterator& other) const { return _it != other._it; }
      Tuple getIndex() const { return _it->first; }
      InstanceClass getInstance() const { return _it->second; }
      std::pair<const Tuple, InstanceClass>& operator*() const { return *_it; }
      std::pair<const Tuple, InstanceClass>* operator->() const { return &(*_it); }

    private:
      typename std::map<Tuple, InstanceClass>::iterator _it;
    };

    iterator begin() const {
      if (instances_.empty()) setInstances();
      return iterator(instances_.begin());
    }

    iterator end() const {
      if (instances_.empty()) setInstances();
      return iterator(instances_.end());
    }
  
    iterator find(Tuple index) const {
      if (instances_.empty()) setInstances();
      return iterator(instances_.find(index));
    }
    

  // For Variant (parameters)
  template <typename T = InstanceClass>
  typename std::enable_if<is_parameter_instance<T>::value, void>::type
  setInstances() const {
    std::map<Tuple, Variant> instances;
    if (isScalar()) {
      AMPL_VARIANT *v;
      AMPL_CALL_CPP(AMPL_GetValue(ampl_, name_.c_str(), &v));
      Variant vpp = Variant::getVar(v);
      AMPL_VariantFree(&v);
      instances.insert(std::pair<Tuple, Variant>(ampl::Tuple(), vpp));
      instances_ = instances;
      return;
    }
    AMPL_TUPLE **tuples;
    size_t size;
    AMPL_CALL_CPP(AMPL_EntityGetTuples(ampl_, name_.c_str(), &tuples, &size));
    for (size_t i = 0; i < size; i++) {
      char *name_c;
      AMPL_VARIANT *v;
      AMPL_CALL_CPP(AMPL_InstanceGetName(ampl_, name_.c_str(), tuples[i], &name_c));
      AMPL_CALL_CPP(AMPL_GetValue(ampl_, name_c, &v));
      Variant vpp = Variant::getVar(v);
      AMPL_VariantFree(&v);
      Tuple tuple(tuples[i]);
      instances.insert(std::pair<Tuple, Variant>(tuple, vpp));
      AMPL_StringFree(&name_c);
      releaseTuple(tuples[i]);
    }
    if (tuples) free(tuples);

    if (size == 0) {
      AMPL_VARIANT *v;
      AMPL_CALL_CPP(AMPL_GetValue(ampl_, name_.c_str(), &v));
      Variant vpp = Variant::getVar(v);
      AMPL_VariantFree(&v);
      instances.insert(std::pair<Tuple, Variant>(ampl::Tuple(), vpp));
    }

    instances_ = instances;
  }

  // For Variables, Constraints, etc.
  template <typename T = InstanceClass>
  typename std::enable_if<!is_parameter_instance<T>::value, void>::type
  setInstances() const {
    std::map<Tuple, InstanceClass> instances;
    if (isScalar()) {
      instances.insert(std::pair<Tuple, InstanceClass>(Tuple(), get()));
      instances_ = instances;
      return;
    }
    AMPL_TUPLE **tuples;
    size_t size;
    AMPL_CALL_CPP(AMPL_EntityGetTuples(ampl_, name_.c_str(),
                         &tuples, &size));
    for (size_t i = 0; i < size; i++) {
      Tuple tuple(tuples[i]);
      InstanceClass instance(ampl_, tuple.impl(), name_);
      instances.insert(std::pair<Tuple, InstanceClass>(tuple, instance));
    }
    for (size_t i = 0; i < size; i++) AMPL_TupleFree(&tuples[i]);
    free(tuples);
    instances_ = instances;
  }


  double getDoubleSuffix(std::string suffix) {
    if (!isScalar())
      throw ampl::UnsupportedOperationException("Not valid for not scalar entities.");
    return get().getDoubleSuffix(suffix);
  }

  std::string getStringSuffix(std::string suffix) {
    if (!isScalar())
      throw ampl::UnsupportedOperationException("Not valid for not scalar entities.");
    return get().getStringSuffix(suffix);
  }

  void setSuffix(std::string suffix, double value) {
    if (!isScalar())
      throw ampl::UnsupportedOperationException("Not valid for not scalar entities.");
    Entity::setSuffix(suffix, value);
  }

  void setSuffix(std::string suffix, std::string value) {
    if (!isScalar())
      throw ampl::UnsupportedOperationException("Not valid for not scalar entities.");
    Entity::setSuffix(suffix, value);
  }

  //@}

  /**
   * Constructor allowing cross conversions
   */
  explicit BasicEntity(::AMPL *ampl, std::string name) : Entity(ampl, name) {}

 private:
  mutable std::map<Tuple, InstanceClass> instances_;
  friend class Entity;
};

/**
 * Represents a list of entities, to be passed as arguments to various API
 *functions
 */
class EntityArgs {
 public:
  /**
   * Constructor from entities
   *
   * @param arg0 First entity
   */
  EntityArgs(Entity arg0) { entities_.push_back(arg0); }

  /**
   * Constructor from entities
   *
   * @param arg0 First entity
   * @param arg1 Second entity
   */
  EntityArgs(Entity arg0, Entity arg1) {
    entities_.push_back(arg0);
    entities_.push_back(arg1);
  }

  /**
   * Constructor from entities
   *
   * @param arg0 First entity
   * @param arg1 Second entity
   * @param arg2 Third entity
   */
  EntityArgs(Entity arg0, Entity arg1, Entity arg2) {
    entities_.push_back(arg0);
    entities_.push_back(arg1);
    entities_.push_back(arg2);
  }

  /**
   * Constructor from entities
   *
   * @param arg0 First entity
   * @param arg1 Second entity
   * @param arg2 Third entity
   * @param arg3 Fourth entity
   */
  EntityArgs(Entity arg0, Entity arg1, Entity arg2, Entity arg3) {
    entities_.push_back(arg0);
    entities_.push_back(arg1);
    entities_.push_back(arg2);
    entities_.push_back(arg3);
  }

  /**
   * Constructor from an array of entities
   *
   * @param args An array of entities
   * @param size Size of the array
   */
  EntityArgs(Entity args[], std::size_t size) {
    for (std::size_t i = 0; i < size; i++) entities_.push_back(args[i]);
  }

  /**
  Get access to the represented entities
  */
  const Entity *getArgs() const { return &entities_[0]; }

  /**
  Number of represented entities
  */
  std::size_t size() const { return entities_.size(); }

 private:
  std::vector<Entity> entities_;
};

/**
This class represents an algebraic or logical constraint. In case the
constraint is scalar, its values can be accessed via functions like
Constraint::body and Constraint::dual.
All the %AMPL suffixes for constraints (see
http://www.ampl.com/NEW/suffbuiltin.html) are available through methods of this
class with the same name (and methods of ConstraintInstance for indexed
constraints). <p> Note that, since this class represents both algebraic and
logical constraints, some suffixes might not be available for every entity. <p>
An std::logic_error is thrown if one of such methods is called for
a non-scalar constraint and if a method corresponding to a suffix which is not
supported by the type of the constraint is called.
A runtime error is thrown if any property of an entity which has been deleted
from the underlying interpreter is accessed.
<p>
The instances, represented by the class ConstraintInstance can be accessed via
the operator Constraint::operator[](), via the methods Constraint::get() or
via the iterators provided.
<p>
To gain access to all the values in an entity (for all instances and all
suffixes for that entities), see Entity::getValues() and the
ampl::DataFrame class.
<p>
*/
class Constraint : public BasicEntity<ConstraintInstance> {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    return get().getDoubleSuffix(suffix);
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    return get().getStringSuffix(suffix);
  }

  /**
   * Check if the constraint is a logical constraint. The available suffixes
   * differ between logical and non logical constraints. See
   * http://www.ampl.com/NEW/suffbuiltin.html for a list of the available
   * suffixes for algebraic constraints. The suffixes available for logical
   * constraints are marked on the method description by "Valid only for logical
   * constraints".
   *
   * \return True if logical
   */
  bool isLogical() const {
    bool isLogical;
    AMPL_CALL_CPP(AMPL_ConstraintIsLogical(ampl_, name_.c_str(), &isLogical));
    return isLogical;
  }
  // *************************************** SCALAR constraints
  // *****************************************

  /**
   * Drop all instances in this constraint entity, corresponding to the %AMPL
   * code: `drop constraintname;`
   */
  void drop() { AMPL_CALL_CPP(AMPL_EntityDrop(ampl_, name_.c_str())); }

  /**
   * Restore all instances in this constraint entity, corresponding to the
   * %AMPL code: `restore constraintname;`
   */
  void restore() { AMPL_CALL_CPP(AMPL_EntityRestore(ampl_, name_.c_str())); }

  /**
   * Get the current value of the constraint's body
   */
  double body() const { return get().body(); }

  /**
   * Get the current %AMPL status (dropped, presolved, or substituted out)
   */
  std::string astatus() const { return get().astatus(); }

  /**
   * Get the index in `_var` of "defined variable" substituted out by
   * the constraint
   */
  int defvar() const { return get().defvar(); }

  /**
   * Get the current initial guess for the constraint's dual variable
   */
  double dinit() const { return get().dinit(); }

  /**
   * Get the original initial guess for the constraint's dual variable
   */
  double dinit0() const { return get().dinit0(); }

  /**
   * Get the current value of the constraint's dual variable.
   * <p>
   * Note that dual values are often reset by the underlying %AMPL interpreter
   * by the presolve functionalities triggered by some methods. A possible
   * workaround is to set the option `presolve;` to `false` (see setBoolOption).
   */
  double dual() const { return get().dual(); }

  /**
   * Get the current value of the constraint's lower bound
   */
  double lb() const { return get().lb(); }

  /**
   * Get the current value of the constraint's upper bound
   */
  double ub() const { return get().ub(); }

  /**
   * Get the constraint lower bound sent to the solver (reflecting adjustment
   * for fixed variables)
   */
  double lbs() const { return get().lbs(); }

  /**
   * Get the constraint upper bound sent to the solver (reflecting adjustment
   * for fixed variables)
   */
  double ubs() const { return get().ubs(); }

  /**
   * Get the current dual value associated with the lower bound
   */
  double ldual() const { return get().ldual(); }

  /**
   * Get the current dual value associated with the upper bounds
   */
  double udual() const { return get().udual(); }

  /**
   * Get the slack at lower bound `body - lb`
   */
  double lslack() const { return get().lslack(); }

  /**
   * Get the slack at upper bound `ub - body`
   */
  double uslack() const { return get().uslack(); }

  /**
   * Constraint slack (the lesser of lslack and uslack)
   */
  double slack() const { return get().slack(); }

  /**
   * Get the solver status (basis status of constraint's %slack or artificial
   * variable)
   */
  std::string sstatus() const { return get().sstatus(); }

  /**
   * Get the %AMPL status if not `in`, otherwise solver status
   */
  std::string status() const { return get().status(); }

  /**
   * %Set the value of the dual variable associated to this constraint (valid
   * only if the constraint is scalar). Equivalent to the %AMPL statement:
   *
   * `let c := dual;`
   *
   * Note that dual values are often reset by the underlying %AMPL interpreter
   * by the presolve functionalities triggered by some methods. A possible
   * workaround is to set the option `presolve` to `false` (see setBoolOption).
   *
   * \param dual
   *            The value to be assigned to the dual variable
   */
  void setDual(double dual) { get().setDual(dual); }

  /**
   * Get the %AMPL val suffix. Valid only for logical constraints.
   */
  double val() const { return get().val(); }

 private:
  explicit Constraint(::AMPL *ampl, std::string name)
      : BasicEntity<ConstraintInstance>(ampl, name) {}

  /**
   * Corresponding class inside the DLL boundary
   */
  friend class AMPL;
  friend class EntityMap<Constraint>;
};

/**
 * Represents an %AMPL objective. Note that, in case of a scalar objective, all
 * the properties (corresponding to %AMPL suffixes) of the objective instance
 * can be accessed through methods like Objective::value(). The methods have the
 * same name of the corresponding %AMPL suffixes. See
 * http://www.ampl.com/NEW/suffbuiltin.html for a list of the available
 * suffixes. <p> All these methods throw an std::logic_error if called for a non
 * scalar objective and an std::runtime_error if called on an entity which has
 * been deleted in the underlying intepreter. <p> The instances, represented by
 * the class ObjectiveInstance can be accessed via the operator
 * Objective::operator[](), via the methods Objective::get() or via the
 * iterators provided. <p> To gain access to all the values in an entity (for
 * all instances and all suffixes for that entities), see Entity::getValues()
 * and the DataFrame class.
 */
class Objective : public BasicEntity<ObjectiveInstance> {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    return get().getDoubleSuffix(suffix);
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    return get().getStringSuffix(suffix);
  }

  /**
   * Get the value of the objective instance
   */
  double value() const { return get().value(); }

  /**
   * Return the %AMPL status
   */
  std::string astatus() const { return get().astatus(); }

  /**
   * Return the solver status
   */
  std::string sstatus() const { return get().sstatus(); }

  /**
   * Exit code returned by solver after most recent solve with this objective
   */
  int exitcode() const { return get().exitcode(); }

  /**
   * Result message returned by solver after most recent solve with this
   * objective
   */
  std::string message() const { return get().message(); }

  /**
   * Result string returned by solver after most recent solve with this
   * objective
   */
  std::string result() const { return get().result(); }

  /**
   * Drop this objective
   */
  void drop() { AMPL_CALL_CPP(AMPL_EntityDrop(ampl_, name_.c_str())); }

  /**
   * Restore this objective  (if it had been dropped, no effect
   * otherwise)
   */
  void restore() { AMPL_CALL_CPP(AMPL_EntityRestore(ampl_, name_.c_str())); }

  /**
   * Get the sense of this objective
   * \return true if minimize, false if maximize
   */
  bool minimization() const {
    int sense;
    AMPL_CALL_CPP(AMPL_ObjectiveSense(ampl_, name_.c_str(), &sense));
    return (sense != 0);
  }

 private:
  explicit Objective(::AMPL *ampl, std::string name)
      : BasicEntity<ObjectiveInstance>(ampl, name) {}

  friend class AMPL;
  friend class EntityMap<Objective>;
};

/**
 * Represents an %AMPL parameter. The values can be Double or String (in case of
 * symbolic parameters).
 * <p>
 * Data can be assigned to the parameter using the methods Parameter::set() and
 * Parameter::setValues directly from objects of this class or using
 * AMPL::setData and a DataFrame object.
 */
class Parameter : public BasicEntity<Variant> {
 public:
  using Entity::getValues;
  using Entity::setValues;

  /** @name Instance access
   * Methods to access the instances which are part of this Entity
   */
  //@{
  /**
    * Get the instance corresponding to a scalar entity.
    *
    * \return The corresponding instance.
    * @throws runtime_error if the entity has been deleted in the underlying
    %AMPL interpreter
    * @throws logic_error if the entity is not scalar
    */
  Variant get() const {
    AMPL_VARIANT *v;
    AMPL_CALL_CPP(AMPL_ParameterGetValue(ampl_, name_.c_str(), &v));
    Variant vpp = Variant::getVar(v);
    AMPL_VariantFree(&v);
    return vpp;
  }

  /**
   * Get the instance with the specified index
   *
   * \param index The tuple specifying the index
   * \return The corresponding instance
   * @throws out_of_range if an instance with the specified index does not exist
   * @throws out_of_range if the entity has been deleted in the underlying %AMPL
   * interpreter
   * @throws ampl::UnsupportedOperationException if the entity is scalar
   */
  Variant get(Tuple index) const {
    AMPL_VARIANT *v;
    AMPL_CALL_CPP(AMPL_ParameterInstanceGetValue(ampl_, name_.c_str(),index.impl(), &v));
    Variant vpp = Variant::getVar(v);
    AMPL_VariantFree(&v);
    return vpp;
  }

  Variant operator[](Tuple index) const { return get(index); }

  Variant operator[](Variant v1) { return get(v1); }

  /**
   * Get the instance with the specified index
   */
  Variant get(Variant v1) const {
    Tuple t(v1);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   */
  Variant get(Variant v1, Variant v2) const {
    Tuple t(v1, v2);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   */
  Variant get(Variant v1, Variant v2, Variant v3) const {
    Tuple t(v1, v2, v3);
    return get(t);
  }

  /**
   * Get the instance with the specified index
   *
   * \param v1 The Variant specifying the first element of the indexing tuple
   * \param v2 The Variant specifying the second element of the indexing
   * tuple \param v3 The Variant specifying the third element of the indexing
   * tuple \param v4 The Variant specifying the fourth element of the
   * indexing tuple \return The corresponding instance
   * @throws out_of_range if an instance with the specified index does not exist
   * @throws runtime_error if the entity has been deleted in the underlying
   * %AMPL interpreter
   * @throws ampl::UnsupportedOperationException if the entity is scalar
   */
  Variant get(Variant v1, Variant v2, Variant v3, Variant v4) const {
    Tuple t(v1, v2, v3, v4);
    return get(t);
  }

  //@}

  /**
   * Returns true if the parameter is declared as symbolic
   * (can store both numerical and string values)
   */
  bool isSymbolic() const {
    bool isSymbolic;
    AMPL_CALL_CPP(AMPL_ParameterIsSymbolic(ampl_, name_.c_str(), &isSymbolic));
    return isSymbolic;
  }

  /**
  \rst
  Check if the parameter has a default initial value. In case of the following
  AMPL code:

  .. code-block:: ampl

    param a;
    param b default a;

  the function will return true for parameter ``b``.
  \endrst

  \return True if the parameter has a default initial value. Please note
          that if the parameter has a default expression which refers to
          another parameter which value is not defined, this will return true.
  */
  bool hasDefault() const {
    bool hasDefault;
    AMPL_CALL_CPP(AMPL_ParameterHasDefault(ampl_, name_.c_str(), &hasDefault));
    return hasDefault;
  }

  /**
  \rst
  Assign the values (string or double) to the parameter instances with the
  specified indices, equivalent to the AMPL code:

  .. code-block:: ampl

    let {i in indices} par[i] := values[i];

  \endrst

  \param indices
             an array of indices of the instances to be set
  \param values
             values to set
  \param nvalues
             length of the values array
  @throws logic_error
              If called on a scalar parameter
  */
  void setValues(const Tuple indices[], Args values,
                 std::size_t nvalues) {
    AMPL_ERRORINFO *err = NULL;
    AMPL_TUPLE **index = (AMPL_TUPLE **)malloc(nvalues * sizeof(AMPL_TUPLE *));
    for (std::size_t i = 0; i < nvalues; i++) index[i] = indices[i].impl();
    err = AMPL_ParameterSetSomeArgsValues(ampl_, name_.c_str(), nvalues, index,
                                   values.data());
    free(index);
    AMPL_CALL_CPP(err);
  }

  /**
  \rst
  Assign the specified values to a 2-d parameter, using the two dimensions
  as two indices.

  For example, the :math:`m \times n` matrix:

  .. math::

    `A = \left( \begin{array}{cccc} a_{11} & a_{12} & ... & a_{1n} \\
    a_{21} & a_{22} & ... & a_{2n} \\ ... & ... & ... & ... \\ a_{  m1} &
    a_{m2} & ... & a_{mn} \end{array} \right)`

  can be assigned to the AMPL parameter: ``param A {1..m, 1..n};``
  with the statement ``setValues(A, false)``.

  As an example, to assign the matrix:

  .. math::
    `A = \left( \begin{array}{cccc} 11 & 12  \\
    21 & 22 \\ 31 & 32 \end{array} \right)`

  to the AMPL paramater: ``param A{1..3, 1..2};`` we can use the following
  code:

  .. code-block:: ampl

    ampl.eval("param a{1..3, 1..2};");
    Parameter a = ampl.getParameter("a");

    double values[6];
    double rows[3];
    double cols[2];
    for (int i = 0; i < 3; i++) {
      rows[i] = i + 1;
      for (int j = 0; j < 2; j++)
      values[i * 2 + j] = (i + 1) * 10 + (j + 1);
    }
    for (int i = 0; i < 2; i++)
      cols[i] = i + 1;

    a.setValues(3, rows, 2, cols, values, false);

  \endrst

  \param num_rows Number of rows
  \param row_indices Indices of the rows
  \param num_cols Number of rows
  \param col_indices Indices of the rows
  \param data Values to be assigned
  \param transpose True to transpose the values in the matrix

  @throws logic_error
               If the method is called on a parameter which is not
               two-dimensional
  @throws invalid_argument
              If the size of 'values' do not correspond to the sizes of
              the underlying indices
  */
  void setValues(std::size_t num_rows, Args row_indices,
                 std::size_t num_cols, Args col_indices,
                 const double *data, bool transpose) {
    AMPL_CALL_CPP(AMPL_ParameterSetValuesMatrix(ampl_, name_.c_str(), num_rows,
                                  row_indices.data(), num_cols,
                                  col_indices.data(), data, transpose));
  }

  /**
  Assign the specified n values to this parameter, assigning them to
  the parameter in the same order as the indices in the entity.
  The number of values in the array must be equal to the
  specified size.

  \param	values	Values to be assigned.
  \param n Number of values to be assigned (must be equal to the number
           of instances in this parameter)


  @throws	invalid_argument If trying to assign a string to a
  non symbolic parameter
  @throws logic_error If the number of arguments is not equal to the number
                      of instances in this parameter
  */
  void setValues(Args values, std::size_t n) {
    AMPL_CALL_CPP(AMPL_ParameterSetArgsValues(ampl_, name_.c_str(), n, values.data()));
  }

  /**
  %Set the value of a scalar parameter.

  @throws runtime_error
              if the entity has been deleted in the underlying %AMPL
  @throws logic_error
              if this parameter is not scalar.
  */
  void set(Variant value) {
    AMPL_CALL_CPP(AMPL_ParameterSetValue(ampl_, name_.c_str(), value.impl()));
  }

  /**
  %Set the value of a single instance of this parameter.
  @throws runtime_error
              if the entity has been deleted in the underlying %AMPL
  */
  void set(Variant index, Variant value) {
    Tuple t(index);
    AMPL_CALL_CPP(AMPL_ParameterInstanceSetValue(ampl_, name_.c_str(), t.impl(), value.impl()));
  }

  /**
  %Set the value of a single instance of this parameter.

  @throws runtime_error
              if the entity has been deleted in the underlying %AMPL
  */
  void set(Tuple index, Variant value) {
    AMPL_CALL_CPP(AMPL_ParameterInstanceSetValue(ampl_, name_.c_str(), index.impl(), value.impl()));
  }

 private:
  explicit Parameter(::AMPL *ampl, std::string name) : 
  BasicEntity<Variant>(ampl, name) {}

  /*
  Corresponding class inside the shared library boundary
  */
  friend class AMPL;
  friend class Entity;
  friend class EntityMap<Parameter>;
};

/**
 * Represents an %AMPL set. In case of not indexed sets, this class exposes
 * iterators for accessing its elements. The members of the
 * set are tuples, represented by objects of class ampl::Tuple.
 * <p>
 * All these methods throw an std::logic_error if called for an indexed set.
 * <p>
 * In case of indexed sets, you can gain access to the instances (of class
 * ampl::SetInstance) using the methods Set::get(), using the operator
 * Set::operator[]() or via Set::instances(),  which returns an InstanceRange
 * providing iterators.
 * <p>
 * Data can be assigned to the set using the methods Set::setValues (for
 * non-indexed sets only) or using ampl::setData and an object of class
 * ampl::DataFrame.
 */
class Set : public BasicEntity<SetInstance> {
 public:
  /**
  Class to access the members of this set (valid only for non-indexed sets)
  */
  typedef SetInstance::MemberRange MemberRange;

  /**
  \rst
  Class used to iterate over all the instances of a Set.
  For example, supposing an indexed set ``set A{1..2};`` is defined in an AMPL
  object named ``ampl``::

    ampl::Set A = ampl.getSet("A");
    for (ampl::SetInstance s: A.instances())
      std::cout << s.name() << "\n";

  \endrst
  */
 class InstanceRange {
  friend class Set;
  const Set* parent_;
  explicit InstanceRange(const Set* parent) : parent_(parent) {}

 public:
  /**
  Iterator over instances of an indexed set
  */
  typedef Set::iterator iterator;

  /**
  Get an iterator pointing to the first instance in this set.
  */
  iterator begin() const { return parent_->begin(); }

  /**
  Get an iterator pointing after the last instance in this entity.
  */
  iterator end() const { return parent_->end(); }

  /**
  Searches the current entity for an instance with the
  specified index.
  \return an iterator to the SetInstance if found, otherwise
          InstanceRange::end.
  */
  iterator find(Tuple t) const { return parent_->find(t); }
};

  /**
   * Get the InstanceRange used to iterate over all the instances in
   * a %Set
   */
  InstanceRange instances() const { return InstanceRange(this); }

  /**
  The arity of s, or number of components in each member of this set
  */
  std::size_t arity() const {
    size_t arity;
    AMPL_CALL_CPP(AMPL_SetGetArity(ampl_, name_.c_str(), &arity));
    return arity;
  }

  // **************** SCALAR SETS *******************
  /**
  Get values of this set in a DataFrame. Valid only for non indexed sets.
  \see SetInstance::getValues()
  */
  DataFrame getValues() const;

  /**
  Get  of this %Set. Valid only for non indexed sets.
  \see SetInstance::members()
  */
  MemberRange members() const { return get().members(); }

  /**
  Get the number of tuples in this set. Valid only for non indexed sets.
  */
  std::size_t size() const { return get().size(); }

  /**
  Check wether this set instance contains the specified Tuple.
  Valid only for non indexed sets.
  \param t Tuple to be found
  */
  bool contains(Tuple t) const { return get().contains(t); }

  /**
  %Set values. Valid only for non indexed sets.
  \see SetInstance::setValues()
  */
  void setValues(Args objects, std::size_t n) {
    get().setValues(objects, n);
  }

  /**
  %Set values. Valid only for non indexed sets.
  \see SetInstance::setValues()
  */
  void setValues(const Tuple objects[], std::size_t n) {
    get().setValues(objects, n);
  }

  /**
  %Set values. Valid only for non indexed sets.
  \see SetInstance::setValues()
  */
  void setValues(DataFrame data);

 private:
  // DataFrame getValues(StringArgs suffixes) const;

  explicit Set(::AMPL *ampl, std::string name)
      : BasicEntity<SetInstance>(ampl, name) {}

  /*
  Corresponding class inside the shared library boundary
  */
  friend class AMPL;
  friend class EntityMap<Set>;
};

namespace var {
/**
 * Integrality of variables
 *
 * @see Variable#integrality()
 */
enum Integrality {
  /**
   * Continuous variable
   */
  CONTINUOUS,
  /**
   * Binary  variable
   */
  BINARY,
  /**
   * Integer variable
   */
  INTEGER
};
}  // namespace var

/**
 * Represents an %AMPL decision variable. Note that, in case of a scalar
 * variable, all the properties of the variable instance can be accessed through
 * methods like Variable.value. The methods have the same name of
 * the corresponding %AMPL suffixes. See
 * http://www.ampl.com/NEW/suffbuiltin.html for a list of the available
 * suffixes. <p> All these methods throw an std::logic_error if called for an
 * entity which is not scalar and an std::runtime_error if the entity has been
 * deleted. <p> The instances, represented by the class VariableInstance can be
 * accessed via the operator Variable::operator[](), via the methods
 * Variable::get() or via the iterators provided. <p> To gain access to all the
 * values in an entity (for all instances and all suffixes for that entities),
 * see Entity::getValues() and the DataFrame class.
 */
class Variable : public BasicEntity<VariableInstance> {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    return get().getDoubleSuffix(suffix);
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    return get().getStringSuffix(suffix);
  }

  /**
   * Get the current value of this variable
   */
  double value() const { 
    return get().value(); 
  }

  /**
   * Get the integrality type for this variable
   *
   * \return Type of integrality (integer, binary, continuous)
   */
  var::Integrality integrality() const {
    int integrality;
    AMPL_CALL_CPP(AMPL_VariableGetIntegrality(ampl_, name_.c_str(), &integrality));
    return static_cast<var::Integrality>(integrality);
  }

  /**
   * Fix all instances of this variable to their current value
   */
  void fix() { AMPL_CALL_CPP(AMPL_VariableFix(ampl_, name_.c_str())); }

  /**
   * Fix all instances of this variable to the specified value
   */
  void fix(double value) {
    AMPL_CALL_CPP(AMPL_VariableFixWithValue(ampl_, name_.c_str(), value));
  }

  /**
   * Unfix this variable instances
   */
  void unfix() { AMPL_CALL_CPP(AMPL_VariableUnfix(ampl_, name_.c_str())); }

  // *************************************** SCALAR VARIABLES
  // *****************************************
  /**
  Set the current value of this variable (does not fix it),
  equivalent to the %AMPL command `let`
  \param value Value to be set
  */
  void setValue(double value) { get().setValue(value); }

  /**
  Get the %AMPL status (fixed, presolved, or substituted out)
  */
  std::string astatus() const { return get().astatus(); }

  /**
   * Get the index in `_con` of "defining constraint" used to substitute
   * variable out
   */
  int defeqn() const { return get().defeqn(); }

  /**
   * Get the dual value on defining constraint of variable substituted out
   */
  double dual() const { return get().dual(); }

  /**
   * Get the current initial guess
   */
  double init() const { return get().init(); }

  /**
   * Get the original initial guess (set by `:=` or`default` or by a data
   * statement)
   */
  double init0() const { return get().init0(); }

  /**
   * \rststar
   * Returns the current lower bound. See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double lb() const { return get().lb(); }

  /**
   * \rststar
   * Returns the current lower bound. See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double ub() const { return get().ub(); }

  /**
   * Returns the initial lower bounds, from the var declaration
   */
  double lb0() const { return get().lb0(); }

  /**
   * Returns the initial upper bound, from the var declaration
   */
  double ub0() const { return get().ub0(); }

  /**
   * Returns the weaker lower bound from %AMPL's presolve phase
   */
  double lb1() const { return get().lb1(); }

  /**
   * Returns the weaker upper bound from %AMPL's presolve phase
   */
  double ub1() const { return get().ub1(); }

  /**
   * Returns the stronger lower bound from %AMPL's presolve phase
   */
  double lb2() const { return get().lb2(); }

  /**
   * Returns the stronger upper bound from %AMPL's presolve phase
   */
  double ub2() const { return get().ub2(); }

  /**
   * Returns the reduced cost at lower bound
   */
  double lrc() const { return get().lrc(); }

  /**
   * Returns the reduced cost at upper bound
   */
  double urc() const { return get().urc(); }

  /**
   * \rststar
   * Return the slack at lower bound (``val - lb``). See
   * :ref:`secVariableSuffixesNotes`. \endrststar
   */
  double lslack() const { return get().lslack(); }

  /**
   * \rststar
   *  Return the slack at upper bound (``ub - val``). See
   * :ref:`secVariableSuffixesNotes`. \endrststar
   */
  double uslack() const { return get().uslack(); }

  /**
   * Get the reduced cost (at the nearer bound)
   */
  double rc() const { return get().rc(); }

  /**
   * \rststar
   * Returns the bound slack which is the lesser of lslack() and
   * uslack(). See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double slack() const { return get().slack(); }

  /**
   * Solver status (basis status of variable)
   */
  std::string sstatus() const { return get().sstatus(); }

  /**
   * %AMPL status if not `in`, otherwise solver status
   */
  std::string status() const { return get().status(); }

 private:
  explicit Variable(::AMPL *ampl, std::string name)
      : BasicEntity<VariableInstance>(ampl, name) {}

  /*
  Corresponding class inside the shared library boundary
  */
  friend class AMPL;
  friend class EntityMap<Variable>;
};

}  // namespace ampl

#include "ampl/dataframe.h"

namespace ampl {
inline DataFrame Entity::getValues() const {
  AMPL_DATAFRAME *dataframe;
  AMPL_CALL_CPP(AMPL_EntityGetValues(ampl_, name_.c_str(), NULL, 0, &dataframe));
  DataFrame df(dataframe);
  return df;
}

inline DataFrame Entity::getValues(StringArgs suffixes) const {
  AMPL_DATAFRAME *dataframe;
  AMPL_CALL_CPP(AMPL_EntityGetValues(ampl_, name_.c_str(), suffixes.args(), suffixes.size(),
                       &dataframe));
  DataFrame df(dataframe);
  return df;
}

inline DataFrame Set::getValues() const {
  if (indexarity() != 0)
    throw std::logic_error("This function is valid only for non-indexed sets.");
  return get().getValues();
}

inline void Set::setValues(DataFrame data) {
  if (indexarity() != 0)
    throw std::logic_error("This function is valid only for non-indexed sets.");
  get().setValues(data);
}

inline void Entity::setSuffixes(DataFrame data) {
  AMPL_CALL_CPP(AMPL_EntitySetSuffixes(ampl_, name_.c_str(), data.impl()));
}

inline void Entity::setSuffix(std::string suffix, double value) {
  AMPL_CALL_CPP(AMPL_InstanceSetDoubleSuffix(ampl_, name_.c_str(), nullptr, suffix.c_str(), value));
}

inline void Entity::setSuffix(std::string suffix, std::string value) {
  AMPL_CALL_CPP(AMPL_InstanceSetStringSuffix(ampl_, name_.c_str(), nullptr, suffix.c_str(), value.c_str()));
}

inline DataFrame SetInstance::getValues() const {
  AMPL_DATAFRAME *df_c;
  AMPL_CALL_CPP(AMPL_SetInstanceGetValuesDataframe(ampl_, entityname_.c_str(), key_, &df_c));
  DataFrame df(df_c);
  return df;
}

inline void SetInstance::setValues(DataFrame data) {
  AMPL_CALL_CPP(AMPL_SetInstanceSetValuesDataframe(ampl_, entityname_.c_str(), key_,
                                     data.impl()));
}

inline void Entity::setValues(DataFrame data) {
  AMPL_CALL_CPP(AMPL_EntitySetValues(ampl_, name_.c_str(), data.impl()));
}

inline Entity Instance::entity() const { return Entity(ampl_, entityname_); }
}  // namespace ampl

#endif  // AMPL_ENTITY_H
