#ifndef AMPL_INSTANCE_H
#define AMPL_INSTANCE_H

#include <set>
#include <string>

#include "ampl/ampl_c.h"
#include "ampl/tuple.h"

#ifdef SWIGJAVA
#define INHERITANCE public
#else
#define INHERITANCE protected
#endif

namespace ampl {
class Entity;
template <class InnerInstance>
class BasicInstance;
template <class InstanceClass>
class BasicEntity;

/**
Base class for instances of modelling entities.
*/
class Instance {
  template <typename InstanceClass>
  friend class BasicEntity;

 public:
  /**
  Returns the entity that this instance is part of
  */
  Entity entity() const;

  /**
  Returns the key of this instance
  */
  Tuple key() const {
    return Tuple(key_);
  }

  /**
  Returns the name of this instance
  */
  std::string name() const {
    char *name_c;
    AMPL_CALL_CPP(AMPL_InstanceGetName(ampl_, entityname_.c_str(), key_, &name_c));
    std::string name(name_c);
    AMPL_StringFree(&name_c);
    return name;
  }

  /**
  Returns a string representation of this instance
  */
  std::string toString() const {
    char *c_str;
    AMPL_CALL_CPP(AMPL_InstanceToString(ampl_, entityname_.c_str(), key_, &c_str));
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

  /**
  Returns expand message of this instance
  */
  std::string expand() const {
    char *c_str;
    AMPL_CALL_CPP(AMPL_InstanceExpand(ampl_, entityname_.c_str(), key_, &c_str));
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

  /**
  Constructor for base class conversions
  */
  template <typename InnerInstance>
  Instance(BasicInstance<InnerInstance> instance);

  /**
  Operator for base class conversions
  */
  template <typename InnerInstance>
  Instance& operator=(BasicInstance<InnerInstance> instance);

  /**
   * Destructor
   */
  ~Instance() {
    if (key_) releaseTuple(key_);
  }

  Instance(const Instance& other) { 
    ampl_ = other.ampl_;
    key_ = other.key_;
    entityname_ = other.entityname_;
    if (other.key_) retainTuple(other.key_);
  }

  Instance& operator=(const Instance& other) {
    if (key_) releaseTuple(key_);
    ampl_ = other.ampl_;
    key_ = other.key_;
    entityname_ = other.entityname_;
    if (key_) retainTuple(key_);
    return *this;
  }

 protected:
  ::AMPL *ampl_;
  AMPL_TUPLE *key_;
  std::string entityname_;

  explicit Instance(::AMPL *ampl, AMPL_TUPLE *key, std::string entityname) 
                    : ampl_(ampl), key_(key), entityname_(entityname) {
                      if (key_) retainTuple(key_);
                    }


  /**
  Get a string suffix value
  */
  std::string strvalue(suffix::StringSuffix kind) const {
    char *value;
    AMPL_CALL_CPP(AMPL_InstanceGetStringSuffix(ampl_, entityname_.c_str(), key_, static_cast<AMPL_STRINGSUFFIX>(kind), &value));
    std::string suffix(value);
    AMPL_StringFree(&value);

    return suffix;
  }

  /**
  Get a double suffix value
  */
  double dblvalue(suffix::NumericSuffix kind) const {
    double value;
    AMPL_CALL_CPP(AMPL_InstanceGetDoubleSuffix(ampl_, entityname_.c_str(), key_, static_cast<AMPL_NUMERICSUFFIX>(kind), &value));
    return value;
  }

  /**
  Get an integer suffix value
  */
  int intvalue(suffix::NumericSuffix kind) const {
    int value;
    AMPL_CALL_CPP(AMPL_InstanceGetIntSuffix(ampl_, entityname_.c_str(), key_, static_cast<AMPL_NUMERICSUFFIX>(kind), &value));
    return value;
  }

  void setSuffix(std::string suffix, std::string value) {
    AMPL_CALL_CPP(AMPL_InstanceSetStringSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), value.c_str()));
  }

  void setSuffix(std::string suffix, double value) {
    AMPL_CALL_CPP(AMPL_InstanceSetDoubleSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), value));
  }
};


/**
 * This class represent an instance of a constraint.
 * <p>
 * In general, all %AMPL suffixes for a constraint are available through methods
 * with the same==145510==    by 0x24CA67: testing::internal::MakeAndRegisterTestInfo(char const*, char const*, char const*, char const*, testing::internal::CodeLocation, void const*, void (*)(), void (*)(), testing::internal::TestFactoryBase*) (gtest.cc:2770)

 * name in this class. See http://www.ampl.com/NEW/suffbuiltin.html
 * for a list of the available suffixes.
 * <p>
 * Note that, since this class represents instances of both algebraic and
 * logical constraints, some suffixes might not be available for every instance.
 * If a wrong suffix for the specific class of constraint is accessed, an
 * std::logic_error is thrown. <p> All the accessors in this class throw an
 * std::runtime_error if the instance has been deleted in the underlying %AMPL
 * interpreter.
 */
class ConstraintInstance : public Instance {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    double value;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedDoubleSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &value)
    );
    return value;
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    char *c_str;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedStringSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &c_str)
    );
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }
  
  /**
   Drop this constraint instance, corresponding to the %AMPL code:
   `drop constraintname;`.
   */
  void drop() {
    AMPL_CALL_CPP(AMPL_InstanceDrop(ampl_, entityname_.c_str(), key_));
  }

  /**
   * Restore this constraint instance, corresponding to the
   * %AMPL code: `restore constraintname;`.
   */
  void restore() {
    AMPL_CALL_CPP(AMPL_InstanceRestore(ampl_, entityname_.c_str(), key_));
  }

  /**
   * Get the current value of the constraint's body
   */
  double body() const { return dblvalue(suffix::body); }

  /**
   * Get the current %AMPL status (dropped, presolved, or substituted out)
   */
  std::string astatus() const { return strvalue(suffix::astatus); }

  /**
   * Get the index in `_var` of "defined variable" substituted out by
   * the constraint
   */
  int defvar() const { return intvalue(suffix::defvar); }

  /**
   * Get the current initial guess for the constraint's dual variable
   */
  double dinit() const { return dblvalue(suffix::dinit); }

  /**
   * Get the original initial guess for the constraint's dual variable
   */
  double dinit0() const { return dblvalue(suffix::dinit0); }

  /**
   * Get the current value of the constraint's dual variable.
   * <p>
   * Note that dual values are often reset by the underlying %AMPL interpreter
   * by the presolve functionalities triggered by some methods. A possible
   * workaround is to set the option `presolve;` to `false` (see setBoolOption).
   */
  double dual() const { return dblvalue(suffix::dual); }

  /**
   * Get the current value of the constraint's lower bound
   */
  double lb() const { return dblvalue(suffix::lb); }

  /**
   * Get the current value of the constraint's upper bound
   */
  double ub() const { return dblvalue(suffix::ub); }

  /**
   * Get the constraint lower bound sent to the solver (reflecting adjustment
   * for fixed variables)
   */
  double lbs() const { return dblvalue(suffix::lbs); }

  /**
   * Get the constraint upper bound sent to the solver (reflecting adjustment
   * for fixed variables)
   */
  double ubs() const { return dblvalue(suffix::ubs); }

  /**
   * Get the current dual value associated with the lower bound
   */
  double ldual() const { return dblvalue(suffix::ldual); }

  /**
   * Get the current dual value associated with the upper bounds
   */
  double udual() const { return dblvalue(suffix::udual); }

  /**
   * Get the slack at lower bound `body - lb`
   */
  double lslack() const { return dblvalue(suffix::lslack); }

  /**
   * Get the slack at upper bound `ub - body`
   */
  double uslack() const { return dblvalue(suffix::uslack); }

  /**
   * Constraint slack (the lesser of lslack and uslack)
   */
  double slack() const { return dblvalue(suffix::slack); }

  /**
   * Get the solver status (basis status of constraint's %slack or artificial
   * variable)
   */
  std::string sstatus() const { return strvalue(suffix::sstatus); }

  /**
   * Get the %AMPL status if not `in`, otherwise solver status
   */
  std::string status() const { return strvalue(suffix::status); }

  /**
   * Set the value of the dual variable associated to this constraint.
   * Equivalent to the %AMPL statement:
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
  void setDual(double dual) {
    AMPL_CALL_CPP(AMPL_ConstraintInstanceSetDual(ampl_, entityname_.c_str(), key_, dual));
  }

  /**
   * Get the AMPL val suffix. Valid only for logical constraints.
   */
  double val() const { return dblvalue(suffix::val); }

 private:
  friend class BasicEntity<ConstraintInstance>;
  friend class Constraint;
  explicit ConstraintInstance(::AMPL *ampl, AMPL_TUPLE *key, std::string name)
      : Instance(ampl, key, name) {}
};

/**
 * Represents an objective instance.
 * <p>
 * All %AMPL suffixes for an objective are available through methods with the
 * same name in this class. See http://www.ampl.com/NEW/suffbuiltin.html for a
 * list of the available suffixes.
 * <p>
 * All the accessors in this class throw an std::runtime_error if the instance
 * has been deleted in the underlying AMPL interpreter.
 */
class ObjectiveInstance : public Instance {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    double value;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedDoubleSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &value)
    );
    return value;
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    char *c_str;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedStringSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &c_str)
    );
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

  /**
   * Get the value of the objective instance
   */
  double value() const { return dblvalue(suffix::value); }

  /**
   * Return the %AMPL status
   */
  std::string astatus() const { return strvalue(suffix::astatus); }

  /**
   * Return the solver status
   */
  std::string sstatus() const { return strvalue(suffix::sstatus); }

  /**
   * Exit code returned by solver after most recent solve with this objective
   */
  int exitcode() const { return intvalue(suffix::exitcode); }

  /**
   * Result message returned by solver after most recent solve with this
   * objective
   */
  std::string message() const { return strvalue(suffix::message); }

  /**
   * Result string returned by solver after most recent solve with this
   * objective
   */
  std::string result() const { return strvalue(suffix::result); }

  /**
   * Drop this objective instance
   */
  void drop() {
    AMPL_CALL_CPP(AMPL_InstanceDrop(ampl_, entityname_.c_str(), key_));
  }

  /**
   * Restore this objective instance (if it had been dropped, no effect
   * otherwise)
   */
  void restore() {
    AMPL_CALL_CPP(AMPL_InstanceRestore(ampl_, entityname_.c_str(), key_));
  }

  /**
   * Get the sense of this objective
   * \return true if minimize, false if maximize
   */
  bool minimization() const {
    std::string sense = strvalue(suffix::sense);
    return (sense.compare("minimize") == 0);
  }

 private:
  friend class BasicEntity<ObjectiveInstance>;
  explicit ObjectiveInstance(::AMPL *ampl, AMPL_TUPLE *key, std::string name)
      : Instance(ampl, key, name) {}
};

class DataFrame;  // forward declaration for setValues below
/**
 * A SetInstance object stores the information regarding a specific instance of
 * a set. The instances can be accessed through the function ampl::Set.get
 * of the parent entity.
 * <p>
 * The set contains a collection of ampl::Tuple
 * <p>
 * Data can be assigned using setValues or using
 * AMPL::setData and a DataFrame object.
 * <p>
 * All the accessors in this class throw an std::runtime_error if
 * the instance has been deleted in the underlying %AMPL interpreter.
 */
class SetInstance : public Instance {
 public:
  /**
   * Returns a string representation of this set instance
   */
  std::string toString() const {
    char *c_str;
    AMPL_CALL_CPP(AMPL_SetInstanceToString(ampl_, entityname_.c_str(), key_, &c_str));
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

  /**
   * Get the number of tuples in this set instance
   */
  std::size_t size() { 
    size_t size;
    AMPL_CALL_CPP(AMPL_SetInstanceGetSize(ampl_, entityname_.c_str(), key_, &size));
    return size;
  }

  /**
  The arity of s, or number of components in each member of this set
  */
  std::size_t arity() const { 
    size_t arity;
    AMPL_CALL_CPP(AMPL_SetGetArity(ampl_, entityname_.c_str(), &arity));
    return arity;
  }

  /**
  Check wether this set instance contains the specified Tuple
  \param t Tuple to be found
  */
  bool contains(Tuple t) const {
    bool contains;
    AMPL_CALL_CPP(AMPL_SetInstanceContains(ampl_, entityname_.c_str(), key_, t.impl(), &contains));
    return contains;
  }

  /**
  Class to access the members (tuples) in this set instance
  */
  class MemberRange {
    private:
      AMPL_TUPLE** members_;
      std::size_t size_;

    public:
      explicit MemberRange(SetInstance* impl_)
        : members_(nullptr), size_(0) {
        AMPL_CALL_CPP(
            AMPL_SetInstanceGetValues(
                impl_->ampl_,
                impl_->entityname_.c_str(),
                impl_->key_,
                &members_,
                &size_));
    }

    ~MemberRange() {
        for (std::size_t i = 0; i < size_; ++i)
            if (members_[i]) AMPL_TupleFree(&members_[i]); // release refcount
        free(members_);
    }

    MemberRange(const MemberRange& other) : members_(nullptr), size_(other.size_) {
      if (size_ > 0) {
        members_ = (AMPL_TUPLE**)malloc(size_ * sizeof(AMPL_TUPLE*));
        for (std::size_t i = 0; i < size_; ++i) {
          members_[i] = nullptr;
          if (other.members_[i])
            AMPL_TupleCopy(&members_[i], other.members_[i]);
        }
      }
    }

  MemberRange& operator=(const MemberRange& other) {
    if (this != &other) {
        // Free current tuples
        for (std::size_t i = 0; i < size_; ++i)
            if (members_[i]) AMPL_TupleFree(&members_[i]);
        free(members_);

        // Copy from other
        size_ = other.size_;
        if (size_ > 0) {
            members_ = (AMPL_TUPLE**)malloc(size_ * sizeof(AMPL_TUPLE*));
            for (std::size_t i = 0; i < size_; ++i) {
                members_[i] = nullptr;
                if (other.members_[i]) {
                    AMPL_TupleCopy(&members_[i], other.members_[i]);
                }
            }
        } else {
            members_ = nullptr;
        }
    }
    return *this;
  }


    /**
     * Iterator
     */
    class iterator {
      public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = Tuple;
        using difference_type = std::ptrdiff_t;
        using pointer = void;
        using reference = value_type;

      private:
        AMPL_TUPLE** ptr_;
        explicit iterator(AMPL_TUPLE** ptr) : ptr_(ptr) {}

        friend class MemberRange;

      public:
        /**
         * Dereference — return Tuple BY VALUE
         */
        Tuple operator*() const {
          return Tuple(*ptr_);
        }

      /**
       * Prefix increment
       */
      iterator& operator++() {
        ++ptr_;
        return *this;
      }

      /**
       * Postfix increment
       */
      iterator operator++(int) {
        iterator tmp(*this);
        ++ptr_;
        return tmp;
      }

      bool operator==(const iterator& other) const {
        return ptr_ == other.ptr_;
      }

      bool operator!=(const iterator& other) const {
        return ptr_ != other.ptr_;
      }
    };

    /**
     * Begin iterator
     */
    iterator begin() const { return iterator(members_); }

    /**
     * End iterator
     */
    iterator end() const { return iterator(members_ + size_); }

    /**
     * Size
     */
    std::size_t size() const { return size_; }
  };


  /**
   * Get all members (tuples) in this set instance
   */
  MemberRange members() { return MemberRange(this); }

  /**
  Set the tuples in this set instance using a flattened array.
  The size of the array must be a multiple of the arity of this
  set instance, and each `arity` elements in the array will be
  grouped into a Tuple.
  \param objects An array of doubles or strings to be grouped into tuples
  \param n The number of objects in the array
  */
  void setValues(Args objects, std::size_t n) {
    AMPL_CALL_CPP(AMPL_SetInstanceSetValues(ampl_, entityname_.c_str(), key_, objects.data(), n));
  }

  /**
  Set the tuples in this set instance

  \param objects An array of tuples
  \param n The number of tuples in the array
  */
  void setValues(const Tuple objects[], std::size_t n) {
    std::vector<AMPL_TUPLE*> tuples(n);
    for (std::size_t i = 0; i < n; i++)
      tuples[i] = objects[i].impl();
    AMPL_CALL_CPP(AMPL_SetInstanceSetValuesTuples(ampl_, entityname_.c_str(), key_, tuples.data(), n));
  }

  /**
  \rst

  Set the values in this set instance to the indexing values of
  the passed DataFrame. The number of indexing columns of the
  parameter must be equal to the arity of this set instance.

  For example, considering the following AMPL entities and corresponding
  C++ objects::

  set A := 1..2;
  param p{i in A} := i+10;
  set AA;

  The following is valid::

  ampl::Set A = ampl.getSet("A"), AA = ampl.getSet("AA");
  AA.setValues(A.getValues()); // A has now the members {1, 2}

  \endrst
  */
  void setValues(DataFrame data);

  /**
  Get all the tuples in this set instance in a DataFrame
  */
  DataFrame getValues() const;

 private:
  friend class BasicEntity<SetInstance>;
  explicit SetInstance(::AMPL *ampl, AMPL_TUPLE *key, std::string name)
      : Instance(ampl, key, name) {}
};

/**
 * A decision variable instance. Each member of this class belongs to a single
 * Variable.
 * Note that accessors available here are replicated at Variable level for
 * ease of use when dealing with scalar variables. <p> All %AMPL suffixes for
 * an algebraic variable are available through methods with the same name in
 * this class. See http://www.ampl.com/NEW/suffbuiltin.html for a list of the
 * available suffixes. <p> All the accessors in this class throw an
 * std::runtime_error if the instance has been deleted in the underlying %AMPL
 * interpreter.
 */
class VariableInstance : public Instance {
 public:
  /** 
   *
   */
  double getDoubleSuffix(std::string suffix) {
    double value;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedDoubleSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &value)
    );
    return value;
  }

  /** 
   *
   */
  std::string getStringSuffix(std::string suffix) {
    char *c_str;
    AMPL_CALL_CPP(
      AMPL_InstanceGetUserDefinedStringSuffix(ampl_, entityname_.c_str(), key_, suffix.c_str(), &c_str)
    );
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

  /**
   * Get the current value of this variable
   */
  double value() const { return dblvalue(suffix::value); }

  /**
   * Fix this variable instance to their current value
   */
  void fix() {
    AMPL_CALL_CPP(AMPL_VariableInstanceFix(ampl_, entityname_.c_str(), key_));
  }

  /**
   * Fix this variable instance to the specified value
   */
  void fix(double value) {
    AMPL_CALL_CPP(AMPL_VariableInstanceFixToValue(ampl_, entityname_.c_str(), key_, value));
  }

  /**
   * Unfix this variable instances
   */
  void unfix() {
    AMPL_CALL_CPP(AMPL_VariableInstanceUnfix(ampl_, entityname_.c_str(), key_));
  }

  // *************************************** SCALAR VARIABLES
  // *****************************************
  /**
  Set the current value of this variable (does not fix it),
  equivalent to the %AMPL command `let`
  \param value Value to be set
  */
  void setValue(double value) {
    AMPL_CALL_CPP(AMPL_VariableInstanceSetValue(ampl_, entityname_.c_str(), key_, value));
  }

  /**
  Get the %AMPL status (fixed, presolved, or substituted out)
  */
  std::string astatus() const { return strvalue(suffix::astatus); }

  /**
   * Get the index in `_con` of "defining constraint" used to substitute
   * variable out
   */
  int defeqn() const { return intvalue(suffix::defeqn); }

  /**
   * Get the dual value on defining constraint of variable substituted out
   */
  double dual() const { return dblvalue(suffix::dual); }

  /**
   * Get the current initial guess
   */
  double init() const { return dblvalue(suffix::init); }

  /**
   * Get the original initial guess (set by `:=` or`default` or by a data
   * statement)
   */
  double init0() const { return dblvalue(suffix::init0); }

  /**
   * \rststar
   * Returns the current lower bound. See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double lb() const { return dblvalue(suffix::lb); }

  /**
   * \rststar
   * Returns the current upper bound. See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double ub() const { return dblvalue(suffix::ub); }

  /**
   * Returns the initial lower bounds, from the var declaration
   */
  double lb0() const { return dblvalue(suffix::lb0); }

  /**
   * Returns the initial upper bound, from the var declaration
   */
  double ub0() const { return dblvalue(suffix::ub0); }

  /**
   * Returns the weaker lower bound from %AMPL's presolve phase
   */
  double lb1() const { return dblvalue(suffix::lb1); }

  /**
   * Returns the weaker upper bound from %AMPL's presolve phase
   */
  double ub1() const { return dblvalue(suffix::ub1); }

  /**
   * Returns the stronger lower bound from %AMPL's presolve phase
   */
  double lb2() const { return dblvalue(suffix::lb2); }

  /**
   * Returns the stronger upper bound from %AMPL's presolve phase
   */
  double ub2() const { return dblvalue(suffix::ub2); }

  /**
   * Returns the reduced cost at lower bound
   */
  double lrc() const { return dblvalue(suffix::lrc); }

  /**
   * Returns the reduced cost at upper bound
   */
  double urc() const { return dblvalue(suffix::urc); }

  /**
   * \rststar
   * Return the slack at lower bound (``val - lb``). See
   * :ref:`secVariableSuffixesNotes`. \endrststar
   */
  double lslack() const { return dblvalue(suffix::lslack); }

  /**
   * \rststar
   *  Return the slack at upper bound (``ub - val``). See
   * :ref:`secVariableSuffixesNotes`. \endrststar
   */
  double uslack() const { return dblvalue(suffix::uslack); }

  /**
   * Get the reduced cost (at the nearer bound)
   */
  double rc() const { return dblvalue(suffix::rc); }

  /**
   * \rststar
   * Returns the bound slack which is the lesser of lslack() and
   * uslack(). See :ref:`secVariableSuffixesNotes`.
   * \endrststar
   */
  double slack() const { return dblvalue(suffix::slack); }

  /**
   * Solver status (basis status of variable)
   */
  std::string sstatus() const { return strvalue(suffix::sstatus); }

  /**
   * %AMPL status if not `in`, otherwise solver status
   */
  std::string status() const { return strvalue(suffix::status); }

  /**
   Returns a string representation of this VariableInstance object.
   The format is as follows:

   \rst
   ::

     'var' name attrs ';'
   \endrst

   where ``name`` is the string returned by the
   VariableInstance::name()  method and ``attrs``
   represent attributes similar to those used in variable declarations.
   <p>
   If the lower bound (``lb``) is equal to the upper bound (``ub``), the
   attributes contain ``= lb``.
   <p>
   If the lower bound is not equal to the upper bound and
  ``Double.NEGATIVE_INFINITY`` , the attributes contain ``>= lb``.
   <p>
   If the upper bound is not equal to the lower bound and
  ``Double.POSITIVE_INFINITY``, the attributes contain ``&lt;= ub``.

   <p>
   If the variable is integer, the attributes contain ``integer``.
   <p>
   If the variable is binary, the attributes contain ``binary``.
  */
  std::string toString() const {
    char *c_str;
    AMPL_CALL_CPP(AMPL_VariableInstanceToString(ampl_, entityname_.c_str(), key_, &c_str));
    std::string str(c_str);
    AMPL_StringFree(&c_str);
    return str;
  }

 private:
  friend class BasicEntity<VariableInstance>;
  explicit VariableInstance(::AMPL *ampl, AMPL_TUPLE *key, std::string name)
      : Instance(ampl, key, name) {}
};

template <class InnerInstance>
inline Instance::Instance(BasicInstance<InnerInstance> instance)
    : ampl_(instance.ampl_), key_(instance.key_), 
    entityname_(instance.entityname_)
    {}

template <class InnerInstance>
inline Instance& Instance::operator=(BasicInstance<InnerInstance> instance) {
  ampl_ = instance.ampl_;
  key_ = instance.key_;
  entityname_ = instance.entityname_;
  return *this;
}
}  // namespace ampl
#endif  // AMPL_INSTANCE_H
