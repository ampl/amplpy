# -*- coding: utf-8 -*-
import sys
import os

_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_vendor_dir = os.path.join(_parent_dir, "vendor")
if _vendor_dir not in sys.path:
    sys.path.append(_vendor_dir)

try:
    from ampltools import *
    from ampltools import __version__
except ImportError:
    print(
        "Failed to import 'ampltools'. Install or upgrade with:\n"
        "   $ python -m pip install ampltools --upgrade\n"
    )
    raise

try:
    from ampltools import _SUPPORT_MESSAGE
except Exception:
    pass