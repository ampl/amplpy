#ifndef AMPL_DECLARATIONS_H
#define AMPL_DECLARATIONS_H

#include <cstring>  // for std::memcpy

#include "ampl/cstringref.h"

#ifdef _WIN32
#ifdef AMPLAPI_EXPORTS
#define AMPLAPI __declspec(dllexport)
#else
#define AMPLAPI __declspec(dllimport)
#endif
#else
#define AMPLAPI __attribute__((visibility("default")))
#endif

namespace ampl {

enum EntityType {
  VARIABLE,
  CONSTRAINT,
  OBJECTIVE,
  PARAMETER,
  SET,
  TABLE,
  PROBLEM,
  UNDEFINED
};
namespace suffix {
enum StringSuffix { astatus = 0, sstatus, status, message, result, sense };
enum NumericSuffix {
  value = 0,
  defeqn,
  dual,
  init,
  init0,
  lb,
  ub,
  lb0,
  ub0,
  lb1,
  ub1,
  lb2,
  ub2,
  lrc,
  urc,
  lslack,
  uslack,
  rc,
  slack,

  // CONSTRAINTS
  body,
  defvar,
  dinit,
  dinit0,
  lbs,
  ubs,
  ldual,
  udual,
  val,  // for logical constraints

  // OBJECTIVES
  exitcode,

};
}  // namespace suffix
}  // namespace ampl

#endif  // AMPL_DECLARATIONS_H
