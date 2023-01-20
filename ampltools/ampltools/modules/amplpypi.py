# -*- coding: utf-8 -*-
import sys
import os


def _normalize_modules(modules=[], add_base=False, skip_base=False):
    prefix = "ampl_module_"
    names = [module.replace("-", "_").replace(prefix, "") for module in modules]
    module_names = [prefix + "base"] if add_base else []
    skip = ["ampl", "base"] if add_base or skip_base else []
    module_names += [prefix + name for name in names if name not in skip]
    return module_names


def installed_modules():
    from pkgutil import iter_modules

    prefix = "ampl_module_"
    installed = []
    for (_, name, _) in iter_modules():
        norm = name.replace("-", "_")
        if norm.startswith(prefix):
            installed.append(norm.replace(prefix, ""))
    return installed


def available_modules():
    from requests import get
    from re import findall

    url = "https://pypi.ampl.com/"
    return [
        l.replace("ampl-module-", "")
        for l in findall(">([^<]+)</a>", get(url).text)
        if l.startswith("ampl-module-")
    ]


def _run_command(cmd, verbose=False):
    from subprocess import check_output, STDOUT, CalledProcessError

    try:
        if verbose:
            print("$ " + " ".join(cmd))
        output = check_output(cmd, stderr=STDOUT).decode("utf-8")
        if verbose:
            print(output)
        return True
    except CalledProcessError as e:
        print(e.output.decode("utf-8"))
        return False


def install_modules(modules=[], reinstall=False, options=[], verbose=False):
    """
    Install AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        reinstall: reinstall modules if True.
        options: list of options for pip.
        verbose: show verbose output if True.
    """
    if isinstance(modules, str):
        modules = [modules]
    available = None
    try:
        available = set(available_modules())
    except Exception:
        pass
    if available:
        for module in modules:
            if "=" in module:
                module = module[: module.find("=")]
            if module not in available:
                raise Exception(f"AMPL module '{module}' is not available.")

    modules = _normalize_modules(modules=modules, add_base=True)
    pip_cmd = [sys.executable, "-m", "pip", "install", "-i", "https://pypi.ampl.com"]
    if reinstall:
        pip_cmd += ["--force-reinstall", "--upgrade", "--no-cache"]
    if not _run_command(pip_cmd + modules + options, verbose=verbose):
        raise Exception("Failed to install modules.")


def uninstall_modules(modules=[], options=[], verbose=False):
    """
    Uninstall AMPL modules for Python.
    Args:
        modules: list of modules to be installed.
        options: list of options for pip.
        verbose: show verbose output if True.
    """
    if isinstance(modules, str):
        modules = [modules]
    skip_base = True
    installed = installed_modules()
    if modules == ["all"]:
        skip_base = False
        modules = installed
    if skip_base and "base" in modules:
        if set(modules) != set(installed):
            raise Exception(
                "Base module cannot be uninstalled alone. "
                "You need to uninstall all modules."
            )
        else:
            skip_base = False

    modules = _normalize_modules(modules=modules, skip_base=skip_base)
    pip_cmd = [sys.executable, "-m", "pip", "uninstall", "-y"]
    if not _run_command(pip_cmd + modules + options, verbose=verbose):
        raise Exception("Failed to uninstall modules.")


def _load_ampl_module(module_name):
    from importlib import import_module

    prefix = "ampl_module_"
    if not module_name.startswith(prefix):
        module_name = prefix + module_name
    module = import_module(module_name)
    return module.bin_dir, module.__version__


def _locate_modules(modules, verbose=False):
    path_modules = []
    for name in modules:
        module_name = "ampl_module_" + name
        bin_dir, _ = _load_ampl_module(module_name)
        if bin_dir not in path_modules:
            path_modules.append(bin_dir)
        if verbose:
            print(f"Imported {module_name}.")

    return path_modules


def _sort_modules_for_loading(modules=[]):
    if isinstance(modules, str):
        modules = [modules]
    if modules == [] or "all" in modules:
        modules = installed_modules()
    return ["base"] + [module for module in modules if module not in ("ampl", "base")]


def generate_requirements(modules=[]):
    """
    Generate requirements.txt content.
    Args:
        modules: list of modules.
        verbose: show verbose output if True.
    """
    modules = _sort_modules_for_loading(modules)
    requirements = "--index-url https://pypi.ampl.com\n"
    requirements += "--extra-index-url https://pypi.org/simple\n"
    for m in modules:
        _, version = _load_ampl_module(m)
        requirements += f"ampl_module_{m}=={version}\n"
    return requirements


def load_modules(modules=[], head=True, verbose=False):
    """
    Load AMPL modules.
    Args:
        modules: list of modules to be loaded.
        head: add to the head of PATH if True.
        verbose: show verbose output if True.
    """
    path_modules = []
    path_others = []
    for path in os.environ["PATH"].split(os.pathsep):
        if path.endswith("bin") and "ampl_module_" in path:
            path_modules.append(path)
        else:
            path_others.append(path)

    modules = _sort_modules_for_loading(modules)
    for path in _locate_modules(modules, verbose=verbose):
        if path not in path_modules:
            path_modules.append(path)

    if head:
        os.environ["PATH"] = os.pathsep.join(path_modules + path_others)
    else:
        os.environ["PATH"] = os.pathsep.join(path_others + path_modules)


def path(modules=[]):
    """
    Return PATH for AMPL modules.
    Args:
        modules: list of modules to be included.
        verbose: show verbose output if True.
    """
    modules = _sort_modules_for_loading(modules)
    return os.pathsep.join(_locate_modules(modules, verbose=False))
