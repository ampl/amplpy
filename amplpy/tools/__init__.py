# -*- coding: utf-8 -*-
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
vendor_dir = os.path.join(parent_dir, "vendor")
if vendor_dir not in sys.path:
    sys.path.append(vendor_dir)

try:
    from ampltools import *
    from ampltools import __version__
except ImportError:
    print(
        "Failed to import 'ampltools'. Install or upgrade with:\n"
        "   $ python -m pip install ampltools --upgrade\n"
    )
    raise
