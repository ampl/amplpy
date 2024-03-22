# -*- coding: utf-8 -*-


cdef class BaseClass(object):
    cdef AMPLPtr* _c_ampl
    cdef str _name

    def __cinit__(self, AMPL ampl, name):
        self._c_ampl = ampl._c_ampl
        self._name = name

    def to_string(self):
        cdef char* output_c
        AMPL_EntityGetDeclaration(self._c_ampl, self._name.encode('utf-8'), &output_c)
        output = str(output_c.decode('utf-8'))
        AMPL_StringFree(output_c)
        return output

    def __str__(self):
        return self.to_string()

    # Aliases
    toString = to_string
