%extend ampl::Variant{
  PyObject *toPyObject() {
    switch (self->type()) {
    case ampl::STRING:
      return PyString_FromString(self->c_str());
    case ampl::NUMERIC:
      return PyFloat_FromDouble(self->dbl());
    case ampl::EMPTY:
      return Py_None;
    }
    return NULL;
  }
}

%extend ampl::VariantRef{
  PyObject *toPyObject() {
    switch (self->type()) {
    case ampl::STRING:
      return PyString_FromString(self->c_str());
    case ampl::NUMERIC:
      return PyFloat_FromDouble(self->dbl());
    case ampl::EMPTY:
      return Py_None;
    }
    return NULL;
  }
}

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
  int setColumnPyList(fmt::CStringRef header, PyObject *list) {
    if (!PyList_Check(list)) {
      return -1;
    }
    std::size_t size = Py_SIZE(list);
    bool has_numbers = false, has_strings = false;
    for (std::size_t i = 0; i < size; i++) {
      PyObject *item = PyList_GetItem(list, i);
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
      std::vector<const char *> values(size);
      for (std::size_t i = 0; i < size; i++) {
        PyObject *item = PyList_GetItem(list, i);
        values[i] = _PyString_AsString(item);
      }
      self->setColumn(header, ampl::internal::Args(values.data()), size);
    } else if (has_numbers && !has_strings) {
      std::vector<double> values(size);
      for (std::size_t i = 0; i < size; i++) {
        PyObject *item = PyList_GetItem(list, i);
        if (PyInt_Check(item)) {
          values[i] = PyInt_AsLong(item);
        } else if (PyLong_Check(item)) {
          values[i] = PyLong_AsLong(item);
        } else {
          values[i] = PyFloat_AsDouble(item);
        }
      }
      self->setColumn(header, ampl::internal::Args(values.data()), size);
    }
    return 0;
  }
}