%inline %{
ampl::Variant VariantFromPyObject(PyObject *obj) {
    if (PyInt_Check(obj)) {
        return ampl::Variant(PyInt_AsLong(obj));
    } else if (PyLong_Check(obj)) {
        return ampl::Variant(PyLong_AsLong(obj));
    } else if (PyFloat_Check(obj)) {
        return ampl::Variant(PyFloat_AsDouble(obj));
    } else if (PyUnicode_Check(obj) || PyString_Check(obj)) {
        return ampl::Variant(std::string(_PyString_AsString(obj)));
    } else {
        return ampl::Variant();
    }
}

bool SetVariantFromPyObject(PyObject *obj, ampl::Variant *v) {
    *v = VariantFromPyObject(obj);
    return v->type() != ampl::EMPTY;
}

bool SetTupleFromPyObject(PyObject *obj, ampl::Tuple *t) {
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
        if (!SetVariantFromPyObject(item, &args[i])) {
            return false;
        }
    }
    *t = ampl::Tuple(args.data(), args.size());
    return true;
}
%}