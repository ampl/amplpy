# -*- coding: utf-8 -*-
import sys


def install_modules(modules=None, reinstall=False, verbose=False):
    """
    Install AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        verbose: show verbose output if True.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    prefix = "ampl_module_"
    names = [module.replace("-", "_").replace(prefix, "") for module in modules]
    modules = [prefix + "base"] + [
        prefix + name for name in names if name not in ("ampl", "base")
    ]
    pip_cmd = [sys.executable, "-m", "pip", "install", "-i", "https://pypi.ampl.com"]
    if reinstall:
        pip_cmd.append("--upgrade")
    try:
        output = check_output(pip_cmd + modules, stderr=STDOUT).decode("utf-8")
        if verbose:
            print(output)
    except CalledProcessError as e:
        print(e.output.decode("utf-8"))
        raise Exception("Failed to install modules") from None


def load_modules(modules=None, verbose=False):
    """
    Load AMPL modules.
    Args:
        modules: list of modules to be loaded.
        verbose: show verbose output if True.
    """
    from pkgutil import iter_modules
    from importlib import import_module

    prefix = "ampl_module_"
    plugins = []
    for (_, name, _) in iter_modules():
        norm = name.replace("-", "_")
        if norm.startswith(prefix):
            clean = norm.replace(prefix, "")
            if modules is not None:
                if norm in modules and clean not in modules:
                    # Skip any module not listed
                    continue
            if clean in ("base", "ampl"):
                # Skip base module
                continue
            plugins.append(name)

    try:
        import_module(prefix + "base")
        if verbose:
            print(f"Imported {prefix}base.")
    except Exception:
        if verbose:
            print(f"Failed to import {prefix}base.")
        pass
    for plugin in plugins:
        try:
            import_module(plugin)
            if verbose:
                print(f"Imported {plugin}.")
        except Exception:
            if verbose:
                print(f"Failed to import {plugin}.")
