
// This tells SWIG to treat char ** as a special case
%typemap(in) char **{
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **)malloc((size + 1) * sizeof(char *));
    for (i = 0; i < size; i++) {
      PyObject *obj = PyList_GetItem($input,i);
      if (_PyString_Check(obj)) {
        $1[i] = (char *)_PyString_AsString(PyList_GetItem($input,i));
      } else {
        PyErr_SetString(PyExc_TypeError,"list must contain strings");
        free($1);
        return NULL;
      }
    }
    $1[i] = 0;
  }
  else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

// Set argument to NULL before any conversion occurs
%typemap(arginit) char **{
   $1 = NULL;
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) char **{
  free((char *)$1);
}
