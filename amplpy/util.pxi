from cpython.dict cimport PyDict_Check, PyDict_Keys, PyDict_Values
from cpython.unicode cimport PyUnicode_Check
from cpython.unicode cimport PyUnicode_AsUTF8
from cpython.list cimport PyList_GetItem
from cpython.long cimport PyLong_Check, PyLong_AsLong
from cpython.float cimport PyFloat_AsDouble
from cpython.object cimport PyObject
from libcpp cimport bool

cdef void PY_AMPL_CALL(campl.AMPL_ERRORINFO* errorinfo) except *:
    cdef campl.AMPL_ERRORCODE rc
    cdef char* message
    cdef char* source
    if errorinfo:
        rc = campl.AMPL_ErrorInfoGetError(errorinfo)
        if rc == campl.AMPL_INFEASIBILITY_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise InfeasibilityException("InfeasibilityException: " + message.decode('utf-8'))
        elif rc == campl.AMPL_PRESOLVE_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise PresolveException("PresolveException: " + message.decode('utf-8'))
        elif rc == campl.AMPL_LICENSE_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise SystemError(message.decode('utf-8'))
        elif rc == campl.AMPL_FILE_IO_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise IOError(message.decode('utf-8'))
        elif rc == campl.AMPL_UNSUPPORTED_OPERATION_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise TypeError(message.decode('utf-8'))
        elif rc == campl.AMPL_INVALID_SUBSCRIPT_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            source = campl.AMPL_ErrorInfoGetSource(errorinfo)
            raise AMPLException(source.decode('utf-8'), campl.AMPL_ErrorInfoGetLine(errorinfo), campl.AMPL_ErrorInfoGetOffset(errorinfo),
                                          message.decode('utf-8'))
        elif rc == campl.AMPL_SYNTAX_ERROR_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            source = campl.AMPL_ErrorInfoGetSource(errorinfo)
            raise AMPLException(source.decode('utf-8'), campl.AMPL_ErrorInfoGetLine(errorinfo), campl.AMPL_ErrorInfoGetOffset(errorinfo),
                                     message.decode('utf-8'))
        elif rc == campl.AMPL_NO_DATA_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise RuntimeError(message.decode('utf-8'))
        elif rc == campl.AMPL_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise RuntimeError(message.decode('utf-8'))
        elif rc == campl.AMPL_RUNTIME_ERROR:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise RuntimeError(message.decode('utf-8'))
        elif rc == campl.AMPL_LOGIC_ERROR:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise TypeError(message.decode('utf-8'))
        elif rc == campl.AMPL_OUT_OF_RANGE:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise KeyError(message.decode('utf-8'))
        elif rc == campl.AMPL_INVALID_ARGUMENT:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise ValueError(message.decode('utf-8'))
        elif rc == campl.AMPL_STD_EXCEPTION:
            message = campl.AMPL_ErrorInfoGetMessage(errorinfo)
            raise RuntimeError(message.decode('utf-8'))
        else:
            raise RuntimeError("Unknown exception")

cdef campl.AMPL_ERRORINFO* setValues(campl.AMPL* ampl, char* name, campl.AMPL_TUPLE* index, values, size_t size):
    cdef campl.AMPL_ERRORINFO* errorinfo
    cdef campl.AMPL_TUPLE** values_c
    cdef size_t i
    values_c = <campl.AMPL_TUPLE**>malloc(size * sizeof(campl.AMPL_TUPLE*))

    for i in range(size):
        values_c[i] = to_c_tuple(values[i])
    
    errorinfo = campl.AMPL_SetInstanceSetValuesTuples(ampl, name, index, values_c, size)

    for i in range(size):
        campl.AMPL_TupleFree(&values_c[i])
    free(values_c)

    return errorinfo

cdef to_py_variant(campl.AMPL_VARIANT* variant):
    cdef campl.AMPL_TYPE type
    cdef char* value_c
    cdef double real_c
    campl.AMPL_VariantGetType(variant, &type)
    if type == campl.AMPL_STRING:
        campl.AMPL_VariantGetStringValue(variant, &value_c)
        return value_c.decode('utf-8')
    elif type == campl.AMPL_NUMERIC:
        campl.AMPL_VariantGetNumericValue(variant, &real_c)
        if real_c % 1 == 0:
            return int(real_c)
        else:
            return real_c
    else:
        return None

cdef to_py_tuple(campl.AMPL_TUPLE* tuple_c):
    cdef size_t size
    cdef campl.AMPL_VARIANT** variants
    cdef list pylist = []
    campl.AMPL_TupleGetSize(tuple_c, &size)
    campl.AMPL_TupleGetVariantPtr(tuple_c, &variants)
    for i in range(size):
        pylist.append(to_py_variant(variants[i]))
    return tuple(pylist)

cdef campl.AMPL_TUPLE* to_c_tuple(py_tuple):
    cdef size_t i
    cdef campl.AMPL_TUPLE* tuple_c

    if not isinstance(py_tuple, (tuple, list)):
        py_tuple = [py_tuple]

    cdef size_t size = len(py_tuple)
    cdef campl.AMPL_VARIANT** variants = <campl.AMPL_VARIANT**> malloc(size * sizeof(campl.AMPL_VARIANT*))

    for i in range(size):
        variants[i] = to_c_variant(py_tuple[i])

    campl.AMPL_TupleCreate(&tuple_c, size, variants)

    for i in range(size):
        campl.AMPL_VariantFree(&variants[i])

    free(variants)
    return tuple_c

cdef campl.AMPL_VARIANT* to_c_variant(value)  except *:
    cdef campl.AMPL_VARIANT* variant
    if isinstance(value, str):
        campl.AMPL_VariantCreateString(&variant, value.encode('utf-8'))
    elif isinstance(value, Real):
        campl.AMPL_VariantCreateNumeric(&variant, value)
    elif value is None:
        campl.AMPL_VariantCreateEmpty(&variant)
    else:
        raise ValueError(f"unsupported type {type(value)}")
    return variant

cdef create_entity(campl.AMPL_ENTITYTYPE entity_class, AMPL ampl, char* name, campl.AMPL_TUPLE* index, parent):
    if entity_class == campl.AMPL_VARIABLE:
        return Variable.create(ampl, name, index, parent)
    elif entity_class == campl.AMPL_CONSTRAINT:
        return Constraint.create(ampl, name, index, parent)
    elif entity_class == campl.AMPL_OBJECTIVE:
        return Objective.create(ampl, name, index, parent)
    elif entity_class == campl.AMPL_SET:
        return Set.create(ampl, name, index, parent)
    elif entity_class == campl.AMPL_PARAMETER:
        return Parameter.create(ampl, name, index, parent)
    else:
        return Entity.create(ampl, name, index, parent)

cdef campl.AMPL_ERRORINFO* setValuesParamNum(campl.AMPL* ampl, char* name, values):
    cdef campl.AMPL_ERRORINFO* errorinfo
    cdef size_t size = len(values)
    cdef double* values_c = <double*> malloc(size * sizeof(double))
    for i in range(size):
        values_c[i] = values[i]
    errorinfo = campl.AMPL_ParameterSetArgsDoubleValues(ampl, name, size, values_c)
    free(values_c)

    return errorinfo

cdef campl.AMPL_ERRORINFO* setValuesParamStr(campl.AMPL* ampl, char* name, values):
    cdef campl.AMPL_ERRORINFO* errorinfo
    cdef size_t size = len(values)
    cdef char** values_c = <char**> malloc(size * sizeof(char*))
    for i in range(size):
        values_c[i] = strdup(values[i].encode('utf-8'))
    
    errorinfo = campl.AMPL_ParameterSetArgsStringValues(ampl, name, size, values_c)

    for i in range(size):
        free(values_c[i])
    free(values_c)

    return errorinfo

cdef campl.AMPL_ERRORINFO* setValuesPyDict(campl.AMPL* ampl, char* name, dict dicts) except *:
    cdef campl.AMPL_ERRORINFO* errorinfo
    cdef size_t i
    cdef campl.AMPL_TUPLE** indices_c
    cdef char** values_str_c
    cdef double* values_num_c
    cdef PyObject* item

    if not PyDict_Check(dicts):
        raise ValueError("Expected a dictionary")
        
    cdef object d_keys = PyDict_Keys(dicts)
    cdef object d_values = PyDict_Values(dicts)
    cdef size_t size = len(dicts)

    cdef bool has_numbers = False
    cdef bool has_strings = False

    for i in range(size):
        item = PyList_GetItem(d_values, i)
        if item == NULL:
            raise ValueError("Failed to access value")

        if PyUnicode_Check(<object>item):
            has_strings = True
        else:
            has_numbers = True

        if has_numbers and has_strings:
            raise ValueError("All values must be either numbers or strings")
        
    if has_strings and not has_numbers:
        indices_c = <campl.AMPL_TUPLE**> malloc(size * sizeof(campl.AMPL_TUPLE*))
        values_str_c = <char **> malloc(size * sizeof(char*))
        for i in range(size):
            indices_c[i] = to_c_tuple(<object>PyList_GetItem(d_keys, i))
            values_str_c[i] = PyUnicode_AsUTF8(<object>PyList_GetItem(d_values, i))
        errorinfo = campl.AMPL_ParameterSetSomeStringValues(ampl, name, size, indices_c, values_str_c)
        for i in range(size):
            campl.AMPL_TupleFree(&indices_c[i])
        free(indices_c)
        free(values_str_c)
    elif has_numbers and not has_strings:
        indices_c = <campl.AMPL_TUPLE**> malloc(size * sizeof(campl.AMPL_TUPLE*))
        values_num_c = <double *> malloc(size * sizeof(double))
        for i in range(size):
            indices_c[i] = to_c_tuple(<object>PyList_GetItem(d_keys, i))
            item = PyList_GetItem(d_values, i)
            if PyLong_Check(<object>item):
                values_num_c[i] = PyLong_AsLong(<object>item)
            else:
                values_num_c[i] = PyFloat_AsDouble(<object>item)
        errorinfo = campl.AMPL_ParameterSetSomeDoubleValues(ampl, name, size, indices_c, values_num_c)
        for i in range(size):
            campl.AMPL_TupleFree(&indices_c[i])
        free(indices_c)
        free(values_num_c)
    else:
        raise ValueError("Dictionary must contain either all strings or all numbers")
    return errorinfo

cdef void raiseKeyError(campl.AMPL_ENTITYTYPE entity_class, str name) except *:
    if entity_class == campl.AMPL_VARIABLE:
        raise KeyError(f"A variable called {name} cannot be found.")
    elif entity_class == campl.AMPL_CONSTRAINT:
        raise KeyError(f"A constraint called {name} cannot be found.")
    elif entity_class == campl.AMPL_OBJECTIVE:
        raise KeyError(f"An objective called {name} cannot be found.")
    elif entity_class == campl.AMPL_SET:
        raise KeyError(f"A set called {name} cannot be found.")
    elif entity_class == campl.AMPL_PARAMETER:
        raise KeyError(f"A parameter called {name} cannot be found.")
    else: 
        pass
