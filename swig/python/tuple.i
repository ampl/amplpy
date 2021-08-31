/* Convert from C --> Python */
%typemap(out) ampl::TupleRef { 
    const ampl::TupleRef &tuple = $1; // to avoid issues with $1[i];
    std::size_t size = tuple.size();
    if (size != 1) {
        $result = PyTuple_New(size);
    }
    for (std::size_t i = 0; i < size; i++) {
        const ampl::VariantRef &v = tuple[i];
        PyObject *item = NULL;
        switch (v.type()) {
        case ampl::STRING:
            item = PyString_FromString(v.c_str());
            break;
        case ampl::NUMERIC:
            item = PyFloat_FromDouble(v.dbl());
            break;
        case ampl::EMPTY:
            item = Py_None;
            break;
        }
        if (size != 1) {
            PyTuple_SetItem($result, i, item);
        } else {
            $result = item;
        }
    }
}

%typemap(out) ampl::Tuple = ampl::TupleRef;

/* Convert from Python --> C */
%typemap(in) ampl::Tuple {
    if(!SetTupleFromPyObject($input, &$1)) {
        SWIG_exception(SWIG_TypeError, "tuple expected");
    }
}

%typemap(typecheck, precedence=0) ampl::Tuple {
    $1 = PyTuple_Check($input) ? 1 : 0;
}

%typemap(in) ampl::Tuple *{
  /* Check if is a list */
  ampl::Tuple t;
  if (PyList_Check($input)) {
        int size = PyList_Size($input);
        int i = 0;
        $1 = (ampl::Tuple *)malloc(size * sizeof(ampl::Tuple));
        memset($1, 0, size * sizeof(ampl::Tuple));
        for (i = 0; i < size; i++) {
            PyObject *obj = PyList_GetItem($input, i);
            if(!SetTupleFromPyObject(obj, &t)) {
                SWIG_exception(SWIG_TypeError, "tuple expected");
            }
            $1[i] = t;
        }
    } else if(SetTupleFromPyObject($input, &t)) {
        $1 = (ampl::Tuple *)malloc(1 * sizeof(ampl::Tuple));
        memset($1, 0, 1 * sizeof(ampl::Tuple));
        $1[0] = t;
    } else {
        PyErr_SetString(PyExc_TypeError, "not a list");
        return NULL;
    }
}

// Set argument to NULL before any conversion occurs
%typemap(arginit) ampl::Tuple *{
   $1 = NULL;
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) ampl::Tuple *{
    free((ampl::Tuple *)$1);
}
