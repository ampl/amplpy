#ifndef AMPL_NANOARROW_H
#define AMPL_NANOARROW_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdint.h>
#include "ampl/declaration_c.h"
#include "ampl/errorhandler_c.h"


#define ARROW_FLAG_DICTIONARY_ORDERED 1
#define ARROW_FLAG_NULLABLE 2
#define ARROW_FLAG_MAP_KEYS_SORTED 4

struct ArrowSchema {
  // Array type description
  const char* format;
  const char* name;
  const char* metadata;
  int64_t flags;
  int64_t n_children;
  struct ArrowSchema** children;
  struct ArrowSchema* dictionary;

  // Release callback
  void (*release)(struct ArrowSchema*);
  // Opaque producer-specific data
  void* private_data;
};

struct ArrowArray {
  // Array data description
  int64_t length;
  int64_t null_count;
  int64_t offset;
  int64_t n_buffers;
  int64_t n_children;
  const void** buffers;
  struct ArrowArray** children;
  struct ArrowArray* dictionary;

  // Release callback
  void (*release)(struct ArrowArray*);
  // Opaque producer-specific data
  void* private_data;
};

struct ArrowArrayStream {
  int (*get_schema)(struct ArrowArrayStream*, struct ArrowSchema* out);
  int (*get_next)(struct ArrowArrayStream*, struct ArrowArray* out);
  const char* (*get_last_error)(struct ArrowArrayStream*);
  void (*release)(struct ArrowArrayStream*);
  void* private_data;
};

typedef struct AMPL_DataFrameArrow AMPL_DATAFRAMEARROW;


AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameArrowCreate(AMPL_DATAFRAMEARROW **dataframe,
                                          struct ArrowSchema *schema,
                                          struct ArrowArray *array,
                                          int64_t nindices);

AMPLAPI void AMPL_DataFrameArrowFree(AMPL_DATAFRAMEARROW **dataframe);

AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameArrowGetSchema(AMPL_DATAFRAMEARROW *dataframe, struct ArrowSchema **schema);

AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameArrowGetArray(AMPL_DATAFRAMEARROW *dataframe, struct ArrowArray **array);

AMPLAPI AMPL_ERRORINFO *AMPL_DataFrameArrowGetNIndices(AMPL_DATAFRAMEARROW *dataframe, int64_t *nindices);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_NANOARROW_H
