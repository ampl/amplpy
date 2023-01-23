# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    try:
        from ampltools.modules import _main
    except ImportError:
        print(
            "Failed to import 'ampltools.modules'. Install or upgrade with:\n"
            "   $ python -m pip install ampltools --upgrade",
            file=sys.stderr,
        )
        sys.exit(1)
    _main()
