// We never have output double* so i define only in typemap
%typemap(in) double *{
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (double *)malloc(size * sizeof(double));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyFloat_Check(o))
        $1[i] = PyFloat_AsDouble(PyList_GetItem($input,i));
      else {
        PyErr_SetString(PyExc_TypeError, "The input list must contain floating point numbers");
        free($1);
        return NULL;
      }
    }
  }
  else {
    PyErr_SetString(PyExc_TypeError,"The input is not a list");
    return NULL;
  }
}

%typemap(freearg) double *{
  free((double *)$1);
}