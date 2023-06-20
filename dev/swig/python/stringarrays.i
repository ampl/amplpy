
// This tells SWIG to treat char ** as a special case
%typemap(in) char **{
    /* Check if is a list */
    if (PyList_Check($input)) {
        std::size_t size = PyList_Size($input);
        std::size_t i = 0;
        $1 = (char **)malloc((size + 1) * sizeof(char *));
        for (i = 0; i < size; i++) {
            PyObject *obj = PyList_GetItem($input,i);
            if (PyUnicode_Check(obj)) {
                $1[i] = (char *)PyUnicode_AsUTF8(PyList_GetItem($input,i));
            } else {
                PyErr_SetString(PyExc_TypeError, "list must contain strings");
                free($1);
                return NULL;
            }
        }
        $1[i] = 0;
    } else {
        PyErr_SetString(PyExc_TypeError, "not a list");
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

/* Convert from C --> Python */
%typemap(out) ampl::StringRefArray {
    const ampl::StringRefArray &sa = $1; // to avoid issues with $1[i];
    std::size_t size = sa.size();
    $result = PyList_New(size);
    for (std::size_t i = 0; i < size; i++) {
        PyList_SetItem($result, i, PyString_FromString(sa[i]));
    }
}

%typemap(out) ampl::StringArray {
    const ampl::StringArray &sa = $1; // to avoid issues with $1[i];
    std::size_t size = sa.size();
    $result = PyList_New(size);
    for (std::size_t i = 0; i < size; i++) {
        PyList_SetItem($result, i, PyString_FromString(sa[i]));
    }
}