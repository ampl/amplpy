/* Convert from Python --> C */
// %typemap(in) ampl::VariantRef {
//     if (PyFloat_Check($input)) {
//         $1 = ampl::Variant(PyFloat_AsDouble($input));
//     } else if (PyInt_Check($input)) {
//         $1 = ampl::Variant(PyInt_AsLong($input));
//     } else if (PyLong_Check($input)) {
//         $1 = ampl::Variant(PyLong_AsLong($input));
//     } else if (PyUnicode_Check($input)) {
//         $1 = ampl::Variant(_PyString_AsString($input));
//     }
// }

// %typemap(typecheck, precedence=200) ampl::VariantRef {
//     $1 = PyFloat_Check($input) || PyInt_Check($input) || PyLong_Check($input) || PyUnicode_Check($input);
// }

/* Convert from C --> Python */
%typemap(out) ampl::VariantRef {
    double vd;
    int vi;
    switch ($1.type()) {
    case ampl::STRING:
        $result = PyString_FromString($1.c_str());
        break;
    case ampl::NUMERIC:
        vd = $1.dbl();
        vi = int(vd);
        if (vd == vi) {
            $result = PyLong_FromLong(vi);
        } else {
            $result = PyFloat_FromDouble(vd);
        }
        break;
    default:
        $result = Py_None;
    }
}

%typemap(out) ampl::Variant = ampl::VariantRef;