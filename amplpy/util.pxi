

cdef void setValues(campl.AMPL* ampl, str name, campl.AMPL_TUPLE* index, values, size_t size):
    cdef campl.AMPL_TUPLE** values_c
    cdef size_t i
    values_c = <campl.AMPL_TUPLE**>malloc(size * sizeof(campl.AMPL_TUPLE*))

    for i in range(size):
        values_c[i] = to_c_tuple(values[i])
    
    campl.AMPL_SetInstanceSetValuesTuples(ampl, name.encode('utf-8'), index, values_c, size)

    for i in range(size):
        free(values_c[i])
    free(values_c)

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
    cdef campl.AMPL_TUPLE* tuple_c

    if not isinstance(py_tuple, (tuple, list)):
        py_tuple = [py_tuple]

    cdef size_t size = len(py_tuple)
    cdef campl.AMPL_VARIANT** variants = <campl.AMPL_VARIANT**> malloc(size * sizeof(campl.AMPL_VARIANT*))

    for i in range(size):
        variants[i] = to_c_variant(py_tuple[i])

    campl.AMPL_TupleCreate(&tuple_c, size, variants)

    free(variants)
    return tuple_c

cdef campl.AMPL_VARIANT* to_c_variant(value):
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

cdef m(campl.AMPL_ENTITYTYPE entity_class, campl.AMPL* ampl, str name, campl.AMPL_TUPLE* index):
    if entity_class == campl.AMPL_VARIABLE:
        return Variable.create(ampl, name, index)
    elif entity_class == campl.AMPL_CONSTRAINT:
        return Constraint.create(ampl, name, index)
    elif entity_class == campl.AMPL_OBJECTIVE:
        return Objective.create(ampl, name, index)
    elif entity_class == campl.AMPL_SET:
        return Set.create(ampl, name, index)
    elif entity_class == campl.AMPL_PARAMETER:
        return Parameter.create(ampl, name, index)
    else:
        return Entity.create(ampl, name, index)

cdef void setValuesParamNum(campl.AMPL* ampl, str name, values):
    cdef size_t size = len(values)
    cdef double* values_c = <double*> malloc(size * sizeof(double))
    for i in range(size):
        values_c[i] = values[i]
    campl.AMPL_ParameterSetArgsDoubleValues(ampl, name.encode('utf-8'), size, values_c)
    free(values_c)

cdef void setValuesParamStr(campl.AMPL* ampl, str name, values):
    cdef size_t size = len(values)
    cdef char** values_c = <char**> malloc(size * sizeof(char*))
    for i in range(size):
        values_c[i] = strdup(values[i].encode('utf-8'))
    
    campl.AMPL_ParameterSetArgsStringValues(ampl, name.encode('utf-8'), size, values_c)

    for i in range(size):
        free(values_c[i])
    free(values_c)

cdef void setValuesPyDict(campl.AMPL* ampl, str name, dicts):
    cdef campl.AMPL_TUPLE* key_c

    if not isinstance(dicts, dict):
        raise ValueError("Expected a dictionary")
        
    d_keys = dicts.keys()
    d_values = dicts.values()
    size = len(dicts)
    has_numbers = False
    has_strings = False

    for item in d_values:
        if isinstance(item, str):
            has_strings = True
        else:
            has_numbers = True
        if has_numbers and has_strings:
            raise ValueError("All values must be either numbers or strings")
        
    if has_strings and not has_numbers:
        for i, (key, value) in enumerate(dicts.items()):
            key_c = to_c_tuple(key)
            campl.AMPL_ParameterInstanceSetStringValue(ampl, name.encode('utf-8'), key_c, value.encode('utf-8'))
    elif has_numbers and not has_strings:
        for i, (key, value) in enumerate(dicts.items()):
            if isinstance(value, int) or isinstance(value, float):
                key_c = to_c_tuple(key)
                campl.AMPL_ParameterInstanceSetNumericValue(ampl, name.encode('utf-8'), key_c, value)            
            else:
                raise ValueError("Unexpected value type")
    else:
        raise ValueError("Dictionary must contain either all strings or all numbers")

cdef raiseKeyError(campl.AMPL_ENTITYTYPE entity_class, name):
    if entity_class == campl.AMPL_VARIABLE:
        raise KeyError("A variable called {name} cannot be found.")
    elif entity_class == campl.AMPL_CONSTRAINT:
        raise KeyError("A constraint called {name} cannot be found.")
    elif entity_class == campl.AMPL_OBJECTIVE:
        raise KeyError("An objective called {name} cannot be found.")
    elif entity_class == campl.AMPL_SET:
        raise KeyError("A set called {name} cannot be found.")
    elif entity_class == campl.AMPL_PARAMETER:
        raise KeyError("A parameter called {name} cannot be found.")
    else: 
        pass
