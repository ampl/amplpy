%extend ampl::internal::Slice<false>{
    PyObject *toPyList() {
        std::size_t size = self->size();
        PyObject* res = PyList_New(size);
        for (std::size_t i = 0; i < size; i++) {
            const ampl::VariantRef &v = (*self)[i];
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
            PyList_SetItem(res, i, item);
        }
        return res;
    }
}

%extend ampl::DataFrame{
    void setColumnPyList(fmt::CStringRef header, PyObject *list) {
        if (!PyList_Check(list)) {
            throw std::logic_error("Expected a list");
        }
        std::size_t size = Py_SIZE(list);
        bool has_numbers = false, has_strings = false;
        for (std::size_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(list, i);
            if (item == NULL) {
                throw std::logic_error("Failed to access value");
            }
            if (PyUnicode_Check(item) || PyString_Check(item)) {
                has_strings = true;
            } else {
                has_numbers = true;
            }
            if (has_numbers && has_strings) {
                throw std::logic_error("All values must be either numbers or strings");
            }
        }
        if (has_strings) {
            std::vector<const char *> values(size);
            for (std::size_t i = 0; i < size; i++) {
                PyObject *item = PyList_GetItem(list, i);
                values[i] = _PyString_AsString(item);
            }
            self->setColumn(header, ampl::internal::Args(values.data()), size);
        } else if (has_numbers) {
            std::vector<double> values(size);
            for (std::size_t i = 0; i < size; i++) {
                PyObject *item = PyList_GetItem(list, i);
                if (PyInt_Check(item)) {
                    values[i] = PyInt_AsLong(item);
                } else if (PyLong_Check(item)) {
                    values[i] = PyLong_AsLong(item);
                } else {
                    PyErr_Clear();
                    values[i] = PyFloat_AsDouble(item);
                    if (PyErr_Occurred() != NULL) {
                        throw std::logic_error("Failed to cast value to int/float/double");
                    }
                }
            }
            self->setColumn(header, ampl::internal::Args(values.data()), size);
        }
    }
}