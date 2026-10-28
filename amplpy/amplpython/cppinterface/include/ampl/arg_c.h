#ifndef AMPL_ARG_C_H
#define AMPL_ARG_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include "ampl/declaration_c.h"

typedef struct AMPL_Args AMPL_ARGS;

AMPLAPI void retainArgs(AMPL_ARGS *args);
AMPLAPI void releaseArgs(AMPL_ARGS *args);
AMPLAPI int AMPL_ArgsCreateNumeric(AMPL_ARGS **args, const double *values);
AMPLAPI int AMPL_ArgsCreateString(AMPL_ARGS **args, const char *const *values);
AMPLAPI int AMPL_ArgsCopy(AMPL_ARGS **args, AMPL_ARGS *copy);
AMPLAPI int AMPL_ArgsDestroy(AMPL_ARGS **args);
AMPLAPI int AMPL_ArgsGetType(AMPL_ARGS *args, AMPL_TYPE *type);
AMPLAPI int AMPL_ArgsGetDblValues(AMPL_ARGS *args, const double **values);
AMPLAPI int AMPL_ArgsGetStrValues(AMPL_ARGS *args, const char *const **values);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_ARG_C_H
