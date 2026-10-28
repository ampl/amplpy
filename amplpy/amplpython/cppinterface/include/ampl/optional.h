#ifndef AMPL_OPTIONAL_H
#define AMPL_OPTIONAL_H

#include <stdexcept>
#include <cassert>

#include "ampl/macros.h"

namespace ampl {

/**
 * This class encapsulates values which can be tested
 * for null-ness.
 */
template <typename T>
class Optional {
  T value_;
  bool has_value_;

 public:
  /**
   * Constructor of an empty instance
   */
  Optional() : has_value_(false) {}

  /**
   * Constructor
   */
  Optional(const T& value) : value_(value), has_value_(true) {}

  /**
   * The cast to bool returns true if the instance
   * has a value, false otherwise
   */
  explicit operator bool() const { return has_value_; }

  /**
   * Accesses the contained value, returns a reference to the
   * contained value. The behaviour is undefined if the object
   * does not contain a value.
   */
  const T& operator*() const {
    assert(has_value_);
    return value_;
  }

  /**
   * Accesses the contained value, returns a pointer to the
   * contained value. The behaviour is undefined if the object
   * does not contain a value.
   */
  const T* operator->() const {
    assert(has_value_);
    return &value_;
  }

  /**
   * Accesses the contained value, returns a reference to the
   * contained value.
   * @throws std::runtime_error if the object does not contain a value
   */
  const T& value() const {
    if (!has_value_)
      throw std::runtime_error("This Optional object has no value.");
    return value_;
  }
};
}  // namespace ampl
#endif  // AMPL_OPTIONAL_H
