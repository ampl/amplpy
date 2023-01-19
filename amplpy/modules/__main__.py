# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    try:
        from ampltools.modules import _main
    except ImportError:
        print(
            "Failed to import 'ampltools.modules'. Install or upgrade with:\n"
            "   $ python -m pip install ampltools --upgrade"
        )
        sys.exit(1)
    try:
        _main(sys.argv)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
