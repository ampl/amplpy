# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
from builtins import range

# from past.builtins import basestring, unicode


def register_magics(store_name="_ampl_cells", ampl_object=None):
    """
    Register jupyter notebook magics ``%%ampl`` and ``%%ampl_eval``.

    Args:
        store_name: Name of the store where ``%%ampl cells`` will be stored.
        ampl_object: Object used to evaluate ``%%ampl_eval`` cells.
    """
    from IPython.core.magic import Magics, magics_class, cell_magic, line_magic

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
            ampl_object.eval(cell)

        @line_magic
        def get_ampl(self, line):
            """Retrieve the store"""
            return self._store

    get_ipython().register_magics(StoreAMPL)


def multidict(d):
    ncols = min(len(d[k]) for k in d)
    return [list(d.keys())] + [{k: d[k][i] for k in d} for i in range(ncols)]
