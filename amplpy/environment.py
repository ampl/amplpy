# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
# from past.builtins import basestring

from .iterators import EnvIterator
from .base import BaseClass
from . import amplpython


class Environment(BaseClass):
    """
    This class provides access to the environment variables and provides
    facilities to specify where to load the underlying AMPL interpreter.
    """

    def __init__(self, binary_directory=None, binary_name=None):
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
        super(Environment, self).__init__(
            amplpython.Environment(binary_directory, binary_name)
        )

    def __iter__(self):
        return EnvIterator(self._impl)

    def __setitem__(self, name, value):
        """
        Add an environment variable to the environment, or change its value if
        already defined.

        Args:
            name: Name of the environment variable.

            value: Value to be assigned.
        """
        self._impl.put(name, value)

    def __getitem__(self, name):
        """
        Searches the current object for an environment variable called name and
        returns an iterator to it if found, otherwise it returns `None`.
        """
        iterator = self._impl.find(name)
        if iterator == self._impl.end():
            return None
        else:
            return iterator.second()

    def set_bin_dir(self, binary_directory):
        """
        Set the location where AMPL API will search for the AMPL executable.

        Args:
            binary_directory: The directory in which look for the AMPL executable.
        """
        self._impl.setBinDir(binary_directory)

    def get_bin_dir(self):
        """
        Get the location where AMPL API will search for the AMPL executable.
        """
        return self._impl.getBinDir()

    def set_bin_name(self, binary_name):
        """
        Set the name of the AMPL executable.

        Args:
            binary_name: The name of the AMPL executable.
        """
        self._impl.setBinName(binary_name)

    def get_bin_name(self):
        """
        Get the name of the AMPL executable.
        """
        return self._impl.getBinName()

    # Aliases
    getBinDir = get_bin_dir
    getBinName = get_bin_name
    setBinDir = set_bin_dir
    setBinName = set_bin_name
