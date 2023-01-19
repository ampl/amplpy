# -*- coding: utf-8 -*-
from .commands import _main
import sys


if __name__ == "__main__":
    try:
        _main(sys.argv)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
