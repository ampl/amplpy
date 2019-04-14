# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import ctypes
import platform

if platform.system() == 'Windows':
    lib32 = os.path.join(os.path.dirname(__file__), 'lib32')
    lib64 = os.path.join(os.path.dirname(__file__), 'lib64')
    from glob import glob
    try:
        if ctypes.sizeof(ctypes.c_voidp) == 4:
            dllfile = glob(lib32 + '/*.dll')[0]
        else:
            dllfile = glob(lib64 + '/*.dll')[0]
        ctypes.CDLL(dllfile)
    except:
        pass

