import amplpython

class Environment:
    """
    This class provides access to the environment variables and provides
    facilities to specify where to load the underlying AMPL interpreter.
    """

    def __init__(self):
        self._impl = amplpython.Environment()

    def __iter__(self):
        return EnvIterator(self._impl)
