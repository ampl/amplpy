%inline %{
ampl::Variant VariantFromPyObject(PyObject *obj) {
    if (obj == Py_None) {
        return ampl::Variant();
    } else if (PyInt_Check(obj)) {
        return ampl::Variant(PyInt_AsLong(obj));
    } else if (PyLong_Check(obj)) {
        return ampl::Variant(PyLong_AsLong(obj));
    } else if (PyFloat_Check(obj)) {
        return ampl::Variant(PyFloat_AsDouble(obj));
    } else if (PyUnicode_Check(obj) || PyString_Check(obj)) {
        return ampl::Variant(std::string(_PyString_AsString(obj)));
    } else {
        PyErr_Clear();
        double value = PyFloat_AsDouble(obj);
        if (PyErr_Occurred() != NULL) {
            throw std::logic_error("Failed to cast value to int/float/double/string");
        }
        return ampl::Variant(value);
    }
}

void SetTupleFromPyObject(PyObject *obj, ampl::Tuple *t) {
    bool is_tuple = PyTuple_Check(obj);
    bool is_list = !is_tuple && PyList_Check(obj);
    std::size_t size = 1;
    if (is_tuple || is_list) {
        size = Py_SIZE(obj);
    }
    std::vector<ampl::Variant> args(size);
    for (std::size_t i = 0; i < size; i++) {
        PyObject *item;
        if (is_tuple) {
            item = PyTuple_GetItem(obj, i);
        } else if (is_list) {
            item = PyList_GetItem(obj, i);
        } else {
            item = obj;
        }
        args[i] = VariantFromPyObject(item);
    }
    *t = ampl::Tuple(args.data(), args.size());
}
%}