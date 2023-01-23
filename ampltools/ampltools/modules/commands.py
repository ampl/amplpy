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
import sys

ERROR = """
Invalid command.
Valid commands: install, uninstall, list/installed, available, path, requirements, run.
"""
USAGE = """Usage:
- Install modules:
    $ python -m $PACKAGE.modules install <solver 1> <solver 2> ...
    Example: $ python -m $PACKAGE.modules install highs gurobi

- Uninstall modules:
    $ python -m $PACKAGE.modules uninstall <solver 1> <solver 2> ...
    Example: $ python -m $PACKAGE.modules uninstall highs gurobi

- List installed modules:
    $ python -m $PACKAGE.modules installed

- List modules available to be installed:
    $ python -m $PACKAGE.modules available

- Value to append to the environment variable PATH to access modules
    $ python -m $PACKAGE.modules path

- Generate requirements.txt for the modules currently installed
    $ python -m $PACKAGE.modules requirements

- Run command in the same environment as the modules:
    $ python -m $PACKAGE.modules run <command>
    Example: $ python -m $PACKAGE.modules run ampl -v
"""


def _main():
    try:
        _commands(sys.argv)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _commands(args):
    usage = USAGE.replace("$PACKAGE", "amplpy" if "amplpy" in args[0] else "ampltools")
    if len(args) < 2:
        raise Exception(ERROR + usage)
    command, args = args[1].lower(), args[2:]
    if command == "usage":
        print(usage)
    elif command == "install":
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
        raise Exception(ERROR + usage)
