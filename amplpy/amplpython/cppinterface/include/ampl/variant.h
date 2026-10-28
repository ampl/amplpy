#ifndef AMPL_VARIANT_H
#define AMPL_VARIANT_H

#include <cstring>  // for strcmp
#include <string>
#include <vector>
#include <cassert>

#include "ampl/variant_c.h"
#include "ampl/cstringref.h"

namespace ampl {
/**
Represents the type of a value in the %AMPL type system,
used in the Variant class.
*/
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

/** Template class which implements a variant object, with
 * or without ownership semantics. The object can represent
 * a string or a double number, and maps directly to the
 * underlying %AMPL type system.
 * It is not intended to be used directly, please use
 * Variant (with ownership semantics, each object stores the
 * values that it represents) or VariantRef
 * (without ownership semantics, each object is only a reference
 * to values stored elsewhere).
 */
class Variant {

 private:
  AMPL_VARIANT *impl_;

 public:
  /**
  Constructor from POD data type. If the BasicVariant has ownership
  semantics, it owns the POD data (deleting it when the BasicVariant
  is deleted and copying it when it is copied).
  */
  static Variant getVar(AMPL_VARIANT* var) {
    AMPL_TYPE type;
    AMPL_VariantGetType(var, &type);
    if (type == AMPL_NUMERIC) {
      double value;
      AMPL_VariantGetNumericValue(var, &value);
      return Variant(value);
    } else if (type == AMPL_STRING) {
      char *value_c;
      AMPL_VariantGetStringValue(var, &value_c);
      std::string value(value_c);
      return Variant(value);
    } else {
      return Variant();
    }
  }

  explicit Variant(AMPL_VARIANT* var) : impl_(var) { retainVariant(impl_); }

  /**
  Default constructor, creates an empty variant
  */
  Variant() { AMPL_VariantCreateEmpty(&impl_); }

  /**
  Creates a numeric variant with the specified value
  */
  Variant(int value) { AMPL_VariantCreateNumeric(&impl_, value); }
  /**
  Creates a numeric variant with the specified value
  */
  Variant(unsigned value) { AMPL_VariantCreateNumeric(&impl_, value); }
  /**
  Creates a numeric variant with the specified value
  */
  Variant(long value) { AMPL_VariantCreateNumeric(&impl_, value); }
  /**
  Creates a numeric variant with the specified value
  */
  Variant(unsigned long value) { AMPL_VariantCreateNumeric(&impl_, value);  }
  /**
  Creates a numeric variant with the specified value
  */
  Variant(double value) { AMPL_VariantCreateNumeric(&impl_, value); }

  /**
  Creates a string variant which references or owns a copy
  of the specified string
  */
  Variant(const std::string& value) {
    AMPL_VariantCreateString(&impl_, value.c_str());
  }

  /**
  Creates a string variant which references or owns a copy
  of the specified string literal
  */
  Variant(const char* value) { AMPL_VariantCreateString(&impl_, value); }

  /**
  Copy constructor. If ``OWNING`` copy the resources
  */
  Variant(const Variant& other) { AMPL_VariantCopy(&impl_, other.impl_); }

  /**
  Destructor. If ``OWNING`` frees the resources.
  */
  ~Variant() { AMPL_VariantFree(&impl_); }

  /**
  Assignment operator
  */
  Variant& operator=(const Variant& other) {
    AMPL_VariantFree(&impl_);
    AMPL_VariantCopy(&impl_, other.impl_);
    return *this;
  }

  /**
  Returns the pointer to a C string.
  */
  const char* c_str() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    assert(type == AMPL_STRING);
    char *value;
    AMPL_VariantGetStringValue(impl_, &value);
    return value;
  }

  /**
  Returns the size of a C string.
  */
  std::size_t size() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    assert(type == AMPL_STRING);
    char *value;
    AMPL_VariantGetStringValue(impl_, &value);
    return std::strlen(value);
  }

  /**
  Returns the numerical value
  */
  double dbl() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    assert(type == AMPL_NUMERIC);
    double value;
    AMPL_VariantGetNumericValue(impl_, &value);
    return value;
  }

  /**
  Converts an %AMPL variant element to an `std::string` object
  */
  std::string str() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    assert(type == AMPL_STRING);
    char *value;
    AMPL_VariantGetStringValue(impl_, &value);
    return std::string(value);
  }

  /**
  Returns the type of this variant object
  */
  Type type() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    return static_cast<Type>(type); 
  }

  /**
  Returns the type of this variant object
  */
  bool is_empty() const {
    AMPL_TYPE type; 
    AMPL_VariantGetType(impl_, &type);
    return type == AMPL_EMPTY; 
  }

  /**
  Get the inner POD struct
  */
  AMPL_VARIANT *impl() const { return impl_; }

  /**
  Return an %AMPL like representation of this variant. String variants are
  single-quoted, numeric are not.
  */
  std::string toString() const {
    char *c_str;
    AMPL_VariantFormat(impl_, &c_str);
    std::string s(c_str);
    return s;
  }
};  // class BasicVariant

namespace internal {
/**
Comparison function. Returns 0 if lhs==rhs, a positive number if lhs>rhs and
a negative integer if lhs<rhs. Implements normal numeric comparison and
lexicographic string comparison (see std::strcmp). Numeric variant < string
variant) is always true.
*/
inline int compare(Variant lhs, Variant rhs) {
  int result = lhs.type() - rhs.type();
  if (result != 0) return result;

  if (lhs.type() == NUMERIC) {
    if (lhs.dbl() == rhs.dbl()) return 0;
    if ((lhs.dbl() - rhs.dbl()) > 0)
      return 1;
    else
      return -1;
  }
  if (lhs.type() == EMPTY) return 0;
  return std::strcmp(lhs.c_str(), rhs.c_str());
}
}  // namespace internal

/**
Comparison operator.
Implements normal numeric comparison and normal string comparison,
(numeric variant < string variant) is always true.
*/
inline bool operator<(Variant t1, Variant t2) {
  return internal::compare(t1, t2) < 0;
}

/**
Comparison operator.
Implements normal numeric comparison and normal string comparison,
(numeric variant <= string variant) is always true.
*/
inline bool operator<=(Variant t1, Variant t2) {
  return internal::compare(t1, t2) <= 0;
}

/**
Equality operator
*/
inline bool operator==(Variant t1, Variant t2) {
  return internal::compare(t1, t2) == 0;
}

/**
Inequality operator
*/
inline bool operator!=(Variant t1, Variant t2) {
  return internal::compare(t1, t2) != 0;
}

/**
Comparison operator.
Implements normal numeric comparison and normal string comparison,
(string variant > numeric variant) is always true.
*/
inline bool operator>(Variant t1, Variant t2) {
  return internal::compare(t1, t2) > 0;
}

/**
Comparison operator.
Implements normal numeric comparison and normal string comparison,
(string variant >= numeric variant) is always true.
*/
inline bool operator>=(Variant t1, Variant t2) {
  return internal::compare(t1, t2) >= 0;
}
}  // namespace ampl

#endif  // AMPL_VARIANT_H
