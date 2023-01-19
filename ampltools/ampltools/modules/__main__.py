# -*- coding: utf-8 -*-
from .commands import main
import sys


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
