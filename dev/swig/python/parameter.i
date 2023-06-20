%extend ampl::Parameter{
    void setValuesPyDict(PyObject *dict) {
        if (!PyDict_Check(dict)) {
            throw std::logic_error("Expected a dictionary");
        }
        PyObject *d_keys = PyDict_Keys(dict);
        PyObject *d_values = PyDict_Values(dict);
        std::size_t size = Py_SIZE(dict);
        bool has_numbers = false, has_strings = false;
        for (std::size_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(d_values, i);
            if (item == NULL) {
                throw std::logic_error("Failed to access value");
            }
            if (PyUnicode_Check(item)) {
                has_strings = true;
            } else {
                has_numbers = true;
            }
            if (has_numbers && has_strings) {
                throw std::logic_error("All values must be either numbers or strings");
            }
        }
        if (has_strings && !has_numbers) {
            std::vector<ampl::Tuple> keys(size);
            std::vector<const char *> values(size);
            for (std::size_t i = 0; i < size; i++) {
                PyObject *item = PyList_GetItem(d_values, i);
                values[i] = PyUnicode_AsUTF8(item);
                SetTupleFromPyObject(PyList_GetItem(d_keys, i), &keys[i]);
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
                SetTupleFromPyObject(PyList_GetItem(d_keys, i), &keys[i]);
            }
            self->setValues(keys.data(), values.data(), size);
        }
    }
}