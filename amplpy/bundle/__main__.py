# -*- coding: utf-8 -*-
import sys
import os

_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_vendor_dir = os.path.join(_parent_dir, "vendor")
if _vendor_dir not in sys.path:
    sys.path.append(_vendor_dir)

if __name__ == "__main__":
    try:
        from ampltools.bundle import _main
    except ImportError:
        print(
            "Failed to import 'ampltools.bundle'. Install or upgrade with:\n"
            "   $ python -m pip install ampltools --upgrade",
            file=sys.stderr,
        )
        sys.exit(1)
    _main()
