#ifndef AMPL_TUPLE_H
#define AMPL_TUPLE_H

#include "ampl/ampl_c.h"
#include "ampl/variant.h"

namespace ampl {
/**
 * Represents a tuple
 */
class Tuple {
 public:
  /** @name Constructors
   * Constructors for Tuple objects.
   */
  //@{
  /**
   * Construct an empty Tuple
   */
  Tuple() {
    AMPL_TupleCreate(&impl_, 0, NULL);
  }

  /**
   * Get access to the inner immutable object (infrastructure).
   */
  AMPL_TUPLE *impl() const { return impl_; }

  /**
   * Construct a n-Tuple from an array of variants
   */
  Tuple(Variant arguments[], std::size_t N) {
    std::vector<AMPL_VARIANT*> vs(N);
    for (std::size_t i = 0; i < N; i++) vs[i] = arguments[i].impl();
    AMPL_TupleCreate(&impl_, vs.size(), vs.data());
  }

  /**
   * Copy constructor. If ``OWNING`` copy the resources
   */
  Tuple(const Tuple& other) {
    AMPL_TupleCopy(&impl_, other.impl_);
  }

  /**
   * Destructor
   */
  ~Tuple() {
    AMPL_TupleFree(&impl_);
  }

  /**
   * Assignment operator
   */
  Tuple& operator=(const Tuple& other) {
    AMPL_TupleFree(&impl_);
    AMPL_TupleCopy(&impl_, other.impl_);
    return *this;
  }

  /** @name Constructors from variants
   * Constructors from ampl::Variant objects.
   */
  //@{
  Tuple(Variant v1) {
    AMPL_VARIANT *vs[] = {v1.impl()};
    AMPL_TupleCreate(&impl_, 1, vs);
  }

  Tuple(Variant v1, Variant v2) {
    AMPL_VARIANT *vs[] = {v1.impl(), v2.impl()};
    AMPL_TupleCreate(&impl_, 2, vs);
  }

  Tuple(Variant v1, Variant v2, Variant v3) {
    AMPL_VARIANT *vs[] = {v1.impl(), v2.impl(), v3.impl()};
    AMPL_TupleCreate(&impl_, 3, vs);
  }

  /**
   * Construct tuples from variants
   *
   * \param v1 First element
   * \param v2 Second element
   * \param v3 Third element
   * \param v4 Fourth element
   */
  Tuple(Variant v1, Variant v2, Variant v3, Variant v4) {
    AMPL_VARIANT *vs[] = {v1.impl(), v2.impl(), v3.impl(), v4.impl()};
    AMPL_TupleCreate(&impl_, 4, vs);
  }

  /**@}*/  // end constructors from variants group
  /**@}*/  // end constructors group

  /**
   * Construct a tuple from an internal struct (infrastructure)
   */
  explicit Tuple(AMPL_TUPLE *other) : impl_(other) { retainTuple(impl_); }

  /**
   * Get the number of Elements in this tuple
   */
  std::size_t size() const {
    size_t size;
    AMPL_TupleGetSize(impl_, &size);
    return size; 
  }

  /**
   * Return a string representation of this tuple. All elements are formatted
   * as in BasicVariant::toString and comma separated.
   * An empty tuple is returned as "()".
   */
  std::string toString() const {
    char* str;
    AMPL_TupleToString(impl_, &str);
    std::string s(str);
    AMPL_StringFree(&str);
    return s;
  }

  /**
   * Accessor for elements of the tuple
   */
  Variant operator[](std::size_t index) const {
    size_t size;
    AMPL_TupleGetSize(impl_, &size);
    assert(index < size);

    AMPL_VARIANT *v;
    AMPL_TupleGetVariant(impl_, index, &v);
    return Variant(v);
  }

  /**
   * Join two tuples together and forms a new one copying all data
   */
  static Tuple join(Tuple t1, Tuple t2) {
    Tuple t;
    std::size_t size1 = t1.size();
    std::size_t size2 = t2.size();
    AMPL_VARIANT **vs = (AMPL_VARIANT**)malloc((size1 + size2) * sizeof(AMPL_VARIANT*));
    for (std::size_t i = 0; i < size1; i++) {
      AMPL_VARIANT *v;
      AMPL_TupleGetVariant(t1.impl(), i, &v);
      vs[i] = v;
      retainVariant(vs[i]);
    }
    for (std::size_t i = 0; i < size2; i++) {
      AMPL_VARIANT *v;
      AMPL_TupleGetVariant(t2.impl(), i, &v);
      vs[i + size1] = v;
      retainVariant(vs[i]);
    }

    AMPL_TupleCreate(&t.impl_, static_cast<size_t>(size1 + size2), vs);    
    return t;
  }

 private:
  AMPL_TUPLE *impl_;
};

namespace internal {

inline int compare(ampl::Tuple t1, ampl::Tuple t2) {
  if (t1.size() == t2.size()) {
    for (std::size_t i = 0; i < t1.size(); i++) {
      int r = compare(t1[i], t2[i]);
      if (r != 0) return r;
    }
    return 0;
  } else
    return (t1.size() > t2.size()) ? 1 : -1;
}

}  // namespace internal

/** @name Tuple comparison operators
 *   Comparison operators for Tuple
 */
///@{

/**
 * Comparison operator.
 * Returns true if t1.size() < t2.size(). Otherwise
 * implements Variant comparison on all elements considering
 * element 0 as the most significative.
 */
inline bool operator<(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) < 0;
}

/* Comparison operator.
 * Returns true if t1.size() <= t2.size(). Otherwise
 * implements Variant comparison on all elements considering
 * element 0 as the most significative.
 */
inline bool operator<=(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) <= 0;
}

/**
 * Equality operator
 */
inline bool operator==(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) == 0;
}

/**
 * Inequality operator
 */
inline bool operator!=(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) != 0;
}

/**
 * Comparison operator.
 * Returns true if t1.size() > t2.size(). Otherwise
 * implements Variant comparison on all elements considering
 * element 0 as the most significative.
 */
inline bool operator>(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) > 0;
}

/**
 * Comparison operator.
 * Returns true if t1.size() >= t2.size(). Otherwise
 * implements Variant comparison on all elements considering
 * element 0 as the most significative.
 */
inline bool operator>=(Tuple t1, Tuple t2) {
  return internal::compare(t1, t2) >= 0;
}

///@}

}  // namespace ampl

#endif  // AMPL_TUPLE_H
