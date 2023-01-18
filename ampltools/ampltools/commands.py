# -*- coding: utf-8 -*-
import sys
from .amplpypi import install_modules, uninstall_modules
from .amplpypi import list_modules, list_modules_available


def ampltools_main():
    args = sys.argv
    try:
        if args[1] == "install":
            modules = [m for m in args[2:] if not m.startswith("-")]
            options = [o for o in args[2:] if o.startswith("-")]
            install_modules(modules=modules, options=options, verbose=True)
        elif args[1] == "uninstall":
            modules = [m for m in args[2:] if not m.startswith("-")]
            options = [o for o in args[2:] if o.startswith("-")]
            uninstall_modules(modules=modules, options=options, verbose=True)
        elif args[1] == "list":
            names = list_modules(verbose=True)
            if names == []:
                raise Exception("Could not find any modules installed.") from None
            print("You have the following modules installed:")
            for name in sorted(set(names)):
                print(f"\t{name}")
        elif args[1] == "available":
            names = list_modules_available()
            if names == []:
                raise Exception("Could not find any modules for download.") from None
            print("You can install any of the following modules:")
            for name in sorted(set(names)):
                print(f"\t{name}")
        else:
            print(
                "Error: Invalid command! Valid commands: install, uninstall, list, available."
            )
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
