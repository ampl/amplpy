# -*- coding: utf-8 -*-
from .amplpypi import (
    install_modules,
    uninstall_modules,
    installed_modules,
    available_modules,
    generate_requirements,
    load_modules,
    path,
)
import subprocess


def _main(args):
    assert len(args) >= 2
    command, args = args[1].lower(), args[2:]
    if command == "install":
        modules = [m for m in args if not m.startswith("-")]
        options = [o for o in args if o.startswith("-")]
        install_modules(modules=modules, options=options, verbose=True)
    elif command == "uninstall":
        modules = [m for m in args if not m.startswith("-")]
        options = [o for o in args if o.startswith("-")]
        uninstall_modules(modules=modules, options=options, verbose=True)
    elif command in ("list", "installed"):
        names = installed_modules()
        if names == []:
            raise Exception("Could not find any modules installed.")
        print("You have the following modules installed:")
        for name in sorted(set(names)):
            print(f"\t{name}")
    elif command == "available":
        names = available_modules()
        if names == []:
            raise Exception("Could not find any modules for download.")
        print("You can install any of the following modules:")
        for name in sorted(set(names)):
            print(f"\t{name}")
    elif command == "path":
        modules = [m for m in args if not m.startswith("-")]
        print(path(modules))
    elif command == "run":
        load_modules()
        subprocess.run(" ".join(args), shell=True)
    elif command == "requirements":
        modules = [m for m in args if not m.startswith("-")]
        print(generate_requirements(modules))
    else:
        raise Exception(
            "Invalid command! Valid commands: install, uninstall, list/installed, available, path, requirements, run."
        )
