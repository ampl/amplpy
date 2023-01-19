# -*- coding: utf-8 -*-
try:
    from ampltools.modules import *
except ImportError:
    print(
        "Failed to import 'ampltools.modules'. Install or upgrade with:\n"
        "   $ python -m pip install ampltools --upgrade\n"
    )
    raise
