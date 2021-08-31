%extend ampl::Parameter{
    int setValuesPyDict(PyObject *dict) {
        if (!PyDict_Check(dict)) {
            return -1;
        }
        PyObject *d_keys = PyDict_Keys(dict);
        PyObject *d_values = PyDict_Values(dict);
        std::size_t size = Py_SIZE(dict);
        bool has_numbers = false, has_strings = false;
        for (std::size_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(d_values, i);
            if (item == NULL) {
                return -2;
            }
            if (PyFloat_Check(item) || PyInt_Check(item) || PyLong_Check(item)) {
                has_numbers = true;
                if (has_strings) return -3;
            } else if (PyUnicode_Check(item) || PyString_Check(item)) {
                has_strings = true;
                if (has_numbers) return -4;
            }
        }
        if (has_strings && !has_numbers) {
            std::vector<ampl::Tuple> keys(size);
            std::vector<const char *> values(size);
            for (std::size_t i = 0; i < size; i++) {
                PyObject *item = PyList_GetItem(d_values, i);
                values[i] = _PyString_AsString(item);
                if (!SetTupleFromPyObject(PyList_GetItem(d_keys, i), &keys[i])) {
                    return -5;
                }
            }
            self->setValues(keys.data(), values.data(), size);
        } else if (has_numbers && !has_strings) {
            std::vector<ampl::Tuple> keys(size);
            std::vector<double> values(size);
            for (std::size_t i = 0; i < size; i++) {
                PyObject *item = PyList_GetItem(d_values, i);
                if (PyInt_Check(item)) {
                    values[i] = PyInt_AsLong(item);
                } else if (PyLong_Check(item)) {
                    values[i] = PyLong_AsLong(item);
                } else {
                    values[i] = PyFloat_AsDouble(item);
                }
                if (!SetTupleFromPyObject(PyList_GetItem(d_keys, i), &keys[i])) {
                    return -6;
                }
            }
            self->setValues(keys.data(), values.data(), size);
        }
        return 0;
    }
}