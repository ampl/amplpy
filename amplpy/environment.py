# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from .iterators import EnvIterator
from .base import BaseClass
from . import amplpython


class Environment(BaseClass):
    """
    This class provides access to the environment variables and provides
    facilities to specify where to load the underlying AMPL interpreter.
    """

    def __init__(self, binaryDirectory=None):
        """
        Constructor with ability to select the location of the AMPL binary.
        Note that if binaryDirectory is set, the automatic lookup for an AMPL
        executable will not be executed.

        Args:
            binaryDirectory: The directory in which look for the AMPL Binary.
        """
        if binaryDirectory is None:
            self._impl = amplpython.Environment()
        else:
            self._impl = amplpython.Environment(binaryDirectory)

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
        it = self._impl.find(name)
        if it == self._impl.end():
            return None
        else:
            return it.second()

    def setBinDir(self, binaryDirectory):
        """
        Set the location where AMPL API will search for the AMPL executable.

        Args:
            binaryDirectory: The directory in which look for the AMPL Binary.
        """
        self._impl.setBinDir(binaryDirectory)

    def getBinDir(self):
        """
        Get the location where AMPL API will search for the AMPL executable.
        """
        return self._impl.getBinDir()
