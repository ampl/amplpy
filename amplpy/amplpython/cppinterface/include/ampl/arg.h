#ifndef AMPL_ARG_H
#define AMPL_ARG_H

#include "ampl/ampl_c.h"
#include "ampl/variant.h"

namespace ampl {
class Tuple;


/**
 * Lightweight class used to pass references to arrays to and from the API
 */
class Args {
 private:
  AMPL_ARGS *data_;
  friend class ampl::Tuple;

 public:
  Args(AMPL_ARGS *data) : data_(data) { retainArgs(data_); }

  Args(const double *values) {
    AMPL_ArgsCreateNumeric(&data_, values);
  }

  Args(const char *const *values) {
    AMPL_ArgsCreateString(&data_, values);
  }

  Args(const Args& other) { AMPL_ArgsCopy(&data_, other.data_); }

  ~Args() { AMPL_ArgsDestroy(&data_); }

  AMPL_ARGS *data() { return data_; }

  Type type() {
    AMPL_TYPE type;
    AMPL_ArgsGetType(data_, &type);
    return static_cast<Type>(type);
  }
};

}  // namespace ampl

#endif  // AMPL_ARG_H
