# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import platform

if platform.system() == 'Windows':
    lib32 = os.path.join(os.path.dirname(__file__), 'lib32')
    lib64 = os.path.join(os.path.dirname(__file__), 'lib64')
    os.environ['PATH'] += os.pathsep + lib32
    os.environ['PATH'] += os.pathsep + lib64


from .amplpython import *
from .amplpython import _READTABLE, _WRITETABLE
