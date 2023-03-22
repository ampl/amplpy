# -*- coding: utf-8 -*-
import sys
import os

_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_vendor_dir = os.path.join(_parent_dir, "vendor")
if _vendor_dir not in sys.path:
    sys.path.append(_vendor_dir)

try:
    from ampltools.modules import *
    from ampltools.modules import __version__
except ImportError:
    print(
        "Failed to import 'ampltools.modules'. Install or upgrade with:\n"
        "   $ python -m pip install ampltools --upgrade\n"
    )
    raise
