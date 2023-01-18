# -*- coding: utf-8 -*-
import sys


def normalize_modules(modules=[], add_base=False, skip_base=False):
    prefix = "ampl_module_"
    names = [module.replace("-", "_").replace(prefix, "") for module in modules]
    module_names = [prefix + "base"] if add_base else []
    skip = ["ampl", "base"] if add_base or skip_base else []
    module_names += [prefix + name for name in names if name not in skip]
    return module_names


def list_modules():
    from pkgutil import iter_modules

    prefix = "ampl_module_"
    installed = []
    for (_, name, _) in iter_modules():
        norm = name.replace("-", "_")
        if norm.startswith(prefix):
            installed.append(norm.replace(prefix, ""))
    return installed


def list_modules_available():
    from bs4 import BeautifulSoup
    from requests import get

    url = "https://pypi.ampl.com/"
    soup = BeautifulSoup(get(url).text, "html.parser")
    names = []
    for link in soup.find_all("a"):
        text = link.string
        if text.startswith("ampl-module-"):
            names.append(text.replace("ampl-module-", ""))
    return names


def install_modules(modules=[], reinstall=False, options=[], verbose=False):
    """
    Install AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        verbose: show verbose output if True.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    modules = normalize_modules(modules=modules, add_base=True)
    pip_cmd = [sys.executable, "-m", "pip", "install", "-i", "https://pypi.ampl.com"]
    if reinstall:
        pip_cmd.append("--upgrade")
        pip_cmd.append("--no-cache")
    try:
        cmd = pip_cmd + modules + options
        output = check_output(cmd, stderr=STDOUT).decode("utf-8")
        if verbose:
            print(output)
    except CalledProcessError as e:
        print(e.output.decode("utf-8"))
        raise Exception("Failed to install modules.") from None


def uninstall_modules(modules=[], options=[], verbose=False):
    """
    Uninstall AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        verbose: show verbose output if True.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    skip_base = True
    if modules == ["all"]:
        skip_base = False
        modules = list_modules_installed()

    modules = normalize_modules(modules=modules, skip_base=skip_base)
    pip_cmd = [sys.executable, "-m", "pip", "uninstall", "-y"]
    try:
        cmd = pip_cmd + modules + options
        output = check_output(cmd, stderr=STDOUT).decode("utf-8")
        if verbose:
            print(output)
    except CalledProcessError as e:
        print(e.output.decode("utf-8"))
        raise Exception("Failed to install modules.") from None


def load_modules(modules=[], verbose=False):
    """
    Load AMPL modules.
    Args:
        modules: list of modules to be loaded.
        verbose: show verbose output if True.
    """
    from importlib import import_module

    prefix = "ampl_module_"
    lst = [module for module in modules if module not in ("ampl", "base")]
    installed = list_modules()
    for module in lst:
        if module not in installed:
            raise Exception(f"Module {module} is missing.")
    plugins = [prefix + module for module in lst]

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
