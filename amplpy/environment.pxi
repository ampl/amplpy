# -*- coding: utf-8 -*-
import os


cdef class Environment(object):
    """
    This class provides access to the environment variables and provides
    facilities to specify where to load the underlying AMPL interpreter.
    """
    cdef campl.AMPL_ENVIRONMENT* _c_env

    def __cinit__(self, binary_directory=None, binary_name=None):
        """
        Constructor with ability to select the location of the AMPL binary.
        Note that if binaryDirectory is set, the automatic lookup for an AMPL
        executable will not be executed.

        Args:
            binary_directory: The directory in which look for the AMPL executable.
            binary_name: The name of the AMPL executable.
        """
        if binary_directory is None:
            binary_directory = ""
        if binary_name is None:
            binary_name = ""
        campl.AMPL_EnvironmentCreate(&self._c_env, binary_directory.encode('utf-8'), binary_name.encode('utf-8'))
        if os.name == "nt":
            # Workaround for Windows issue with environment variables
            for option_name in ["ampl_libpath", "solver"]:
                option_value = os.environ.get(option_name, "")
                if option_value:
                    campl.AMPL_EnvironmentAddEnvironmentVariable(self._c_env, option_name.encode('utf-8'), option_value.encode('utf-8'))

    cdef campl.AMPL_ENVIRONMENT* get_c_pointer(self):
        return self._c_env

    def __dealloc__(self):
        campl.AMPL_EnvironmentFree(&self._c_env)

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        return EnvIterator.create(self._c_env)

    def __setitem__(self, name, value):
        """
        Add an environment variable to the environment, or change its value if
        already defined.

        Args:
            name: Name of the environment variable.

            value: Value to be assigned.
        """
        campl.AMPL_EnvironmentAddEnvironmentVariable(self._c_env, name.encode('utf-8'), value.encode('utf-8'))

    def __getitem__(self, name):
        """
        Searches the current object for an environment variable called name and
        returns an iterator to it if found, otherwise it returns `None`.
        """
        cdef campl.AMPL_ENVIRONMENTVAR* iterator
        cdef char* value_c
        if not campl.AMPL_EnvironmentFindEnvironmentVar(self._c_env, name.encode('utf-8'), &iterator):
            campl.AMPL_EnvironmentVarGetValue(iterator, &value_c)
            value = str(value_c.decode('utf-8'))
            return value
        else:
            return None

    def to_string(self):
        cdef const char* to_string_c
        campl.AMPL_EnvironmentToString(self._c_env, &to_string_c)
        to_string = str(to_string_c.decode('utf-8'))
        return to_string

    def set_bin_dir(self, binary_directory):
        """
        Set the location where AMPL API will search for the AMPL executable.

        Args:
            binary_directory: The directory in which look for the AMPL executable.
        """
        campl.AMPL_EnvironmentSetBinaryDirectory(self._c_env, binary_directory.encode('utf-8'))

    def get_bin_dir(self):
        """
        Get the location where AMPL API will search for the AMPL executable.
        """
        cdef const char* bin_dir_c
        campl.AMPL_EnvironmentGetBinaryDirectory(self._c_env, &bin_dir_c)
        bin_dir = str(bin_dir_c.decode('utf-8'))
        return bin_dir

    def set_bin_name(self, binary_name):
        """
        Set the name of the AMPL executable.

        Args:
            binary_name: The name of the AMPL executable.
        """
        campl.AMPL_EnvironmentSetBinaryName(self._c_env, binary_name.encode('utf-8'))

    def get_bin_name(self):
        """
        Get the name of the AMPL executable.
        """
        cdef const char* bin_name_c
        campl.AMPL_EnvironmentGetBinaryName(self._c_env, &bin_name_c)
        bin_name = str(bin_name_c.decode('utf-8'))
        return bin_name
    
    # Aliases
    toString = to_string
    getBinDir = get_bin_dir
    getBinName = get_bin_name
    setBinDir = set_bin_dir
    setBinName = set_bin_name
