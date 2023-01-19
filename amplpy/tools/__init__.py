# -*- coding: utf-8 -*-
try:
    from ampltools import *
    from ampltools import __version__
except ImportError:
    print(
        "Failed to import 'ampltools'. Install or upgrade with:\n"
        "   $ python -m pip install ampltools --upgrade\n"
    )
    raise
