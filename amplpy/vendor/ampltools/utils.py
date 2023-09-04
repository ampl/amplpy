# -*- coding: utf-8 -*-
import os
from uuid import UUID


def _is_valid_uuid(uuid):
    if uuid in (None, ""):
        return False
    try:
        UUID(str(uuid))
    except ValueError:
        return False

    return True


def add_to_path(path, head=True):
    if head:
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    else:
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + path


def register_magics(store_name="_ampl_cells", ampl_object=None, globals_=None):
    """
    Register jupyter notebook magics ``%%ampl`` and ``%%ampl_eval``.
    Args:
        store_name: Name of the store where ``%%ampl cells`` will be stored.
        ampl_object: Object used to evaluate ``%%ampl_eval`` cells.
    """
    from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
    from IPython import get_ipython

    @magics_class
    class StoreAMPL(Magics):
        def __init__(self, shell=None, **kwargs):
            Magics.__init__(self, shell=shell, **kwargs)
            self._store = []
            shell.user_ns[store_name] = self._store

        @cell_magic
        def ampl(self, line, cell):
            """Store the cell in the store"""
            self._store.append(cell)

        @cell_magic
        def ampl_eval(self, line, cell):
            """Evaluate the cell"""
            if globals_ is not None and isinstance(ampl_object, str):
                ampl = globals_[ampl_object]
            else:
                ampl = ampl_object
            ampl.eval("\n" + cell)

        @line_magic
        def get_ampl(self, line):
            """Retrieve the store"""
            return self._store

    get_ipython().register_magics(StoreAMPL)
