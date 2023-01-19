# -*- coding: utf-8 -*-
from .amplpypi import (
    install_modules,
    uninstall_modules,
    installed_modules,
    available_modules,
)


def _main(args):
    assert len(args) >= 2
    if args[1] == "install":
        modules = [m for m in args[2:] if not m.startswith("-")]
        options = [o for o in args[2:] if o.startswith("-")]
        install_modules(modules=modules, options=options, verbose=True)
    elif args[1] == "uninstall":
        modules = [m for m in args[2:] if not m.startswith("-")]
        options = [o for o in args[2:] if o.startswith("-")]
        uninstall_modules(modules=modules, options=options, verbose=True)
    elif args[1] in ("list", "installed"):
        names = installed_modules()
        if names == []:
            raise Exception("Could not find any modules installed.")
        print("You have the following modules installed:")
        for name in sorted(set(names)):
            print(f"\t{name}")
    elif args[1] == "available":
        names = available_modules()
        if names == []:
            raise Exception("Could not find any modules for download.")
        print("You can install any of the following modules:")
        for name in sorted(set(names)):
            print(f"\t{name}")
    else:
        raise Exception(
            "Invalid command! Valid commands: install, uninstall, list/installed, available."
        )
