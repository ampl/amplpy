# -*- coding: utf-8 -*-
import sys
import os
import tempfile
from .utils import cloud_platform_name


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
    for _, name, _ in iter_modules():
        norm = name.replace("-", "_")
        if norm.startswith(prefix):
            installed.append(norm.replace(prefix, ""))

    # Move bundles to the end to load individual modules first
    low_piority = ["coin", "open"]
    for name in low_piority:
        module_name = prefix + name
        if module_name in installed:
            installed.remove(module_name)
            installed.append(module_name)

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


def _available_bundles():
    from requests import get
    from json import loads

    url = "https://pypi.ampl.com/bundles.json"
    return loads(get(url).text)["bundles"]


def run_command(cmd, show_output=None, return_output=False, verbose=False):
    """
    Run a system command.
    Args:
        cmd: command to run.
        show_output: show the output of running the command.
        verbose: show verbose output if True.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    if isinstance(cmd, str):
        shell = True
        cmd_str = cmd
    else:
        shell = False
        cmd_str = " ".join(cmd)
    if verbose:
        print("$ " + cmd_str)
    try:
        output = check_output(cmd, stderr=STDOUT, shell=shell).decode("utf-8")
        if show_output or verbose:
            print(output.rstrip("\n"))
        if return_output:
            return 0, output
        return 0
    except CalledProcessError as e:
        output = e.output.decode("utf-8")
        if verbose:
            print(output.rstrip("\n"))
        if return_output:
            return e.returncode, output
        return e.returncode


def _parse_module(module):
    if "=" not in module:
        return module, ""
    name, version = (
        module[: module.find("=")].strip(" ="),
        "==" + module[module.find("=") + 1 :].strip(" ="),
    )
    return name, version


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
    bundles = None
    try:
        bundles = _available_bundles()
    except Exception:
        pass
    requirements = modules
    if available:
        requirements = []
        for module in modules:
            version = ""
            if "=" in module:
                module, version = _parse_module(module)
            requirement = module + version
            if requirement in requirements or module == "ampl":
                continue
            elif module in available:
                requirements.append(requirement)
            elif not isinstance(bundles, list):
                requirements.append(requirement)
            else:
                for entry in bundles:
                    bundle, includes = None, []
                    try:
                        bundle = entry["module"]
                        includes = entry["includes"]
                    except:
                        pass
                    if module in includes:
                        raise Exception(
                            f"AMPL module '{module}' is not available. It is included in module '{bundle}'."
                        )
                else:
                    raise Exception(f"AMPL module '{module}' is not available.")

    modules = _normalize_modules(modules=requirements, add_base=True)
    pip_cmd = [sys.executable, "-m", "pip", "install", "-i", "https://pypi.ampl.com"]
    if reinstall:
        pip_cmd += ["--force-reinstall", "--upgrade", "--no-cache"]
    if run_command(pip_cmd + modules + options, verbose=verbose) != 0:
        raise Exception("Failed to install modules.")
    load_modules(modules, verbose=verbose)


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
    if modules == [] or "all" in modules:
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

    unload_modules(modules)
    modules = _normalize_modules(modules=modules, skip_base=skip_base)
    if len(modules) == 0:
        return
    pip_cmd = [sys.executable, "-m", "pip", "uninstall", "-y"]
    if run_command(pip_cmd + modules + options, verbose=verbose) != 0:
        raise Exception("Failed to uninstall modules.")


def _load_ampl_module(module_name):
    from importlib import import_module

    prefix = "ampl_module_"
    if not module_name.startswith(prefix):
        module_name = prefix + module_name
    module = import_module(module_name)
    try:
        from importlib import reload

        reload(module)
    except:
        pass

    mod_file = module.__file__
    if mod_file is None:
        mod_file = ""
    if mod_file.endswith(".pyc"):
        mod_file = mod_file[:-1]
    if not os.path.isfile(mod_file):
        raise Exception(f"Module {module_name} needs to be reinstalled.")

    bin_dir, version = module.bin_dir, module.__version__
    return bin_dir, version


def _locate_modules(modules, verbose=False):
    path_modules = []
    for module_name in modules:
        if not module_name.startswith("ampl_module_"):
            module_name = "ampl_module_" + module_name
        bin_dir = None
        try:
            bin_dir, _ = _load_ampl_module(module_name)
        except:
            if verbose:
                print(f"Failed to import {module_name}.")
            continue
        if bin_dir not in path_modules:
            path_modules.append(bin_dir)
        if verbose:
            print(f"Imported {module_name}.")

    return path_modules


def _sort_modules_for_loading(modules=[], add_base=True):
    if isinstance(modules, str):
        modules = [modules]
    if len(modules) == 0 or "all" in modules:
        modules = installed_modules()
    modules = [_parse_module(module)[0] for module in modules]
    if not add_base:
        return modules
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
        try:
            _, version = _load_ampl_module(m)
            requirements += f"ampl_module_{m}=={version}\n"
        except:
            pass
    return requirements


def _find_ampl_lic():
    for path in os.environ.get("PATH", "").split(os.pathsep):
        ampl_lic = os.path.abspath(os.path.join(path, "ampl.lic"))
        if os.path.isfile(ampl_lic):
            return ampl_lic
    return None


def _prepare_amplkey_env(verbose=False):
    VAR_AMPL_LICFILE = "AMPL_LICFILE"
    VAR_AMPLKEY_RUNTIME_DIR = "AMPLKEY_RUNTIME_DIR"
    if VAR_AMPL_LICFILE in os.environ and VAR_AMPLKEY_RUNTIME_DIR in os.environ:
        # do nothing if all environment variables are set
        return

    bin_dir, _ = _load_ampl_module("base")
    base_ampl_lic = os.path.abspath(os.path.join(bin_dir, "ampl.lic"))
    if os.access(base_ampl_lic, os.W_OK):
        # do nothing if ampl.lic is writable
        return

    if _find_ampl_lic() != base_ampl_lic:
        # do nothing if ampl.lic is somewhere else
        return

    def set_ampl_lic(ampl_lic):
        if verbose:
            print(f'Setting {VAR_AMPL_LICFILE}="{ampl_lic}".')
        os.environ[VAR_AMPL_LICFILE] = ampl_lic

    def set_amplkey_runtime(amplkey_runtime):
        if verbose:
            print(f'Setting {VAR_AMPLKEY_RUNTIME_DIR}="{amplkey_runtime}".')
        os.environ[VAR_AMPLKEY_RUNTIME_DIR] = amplkey_runtime

    if verbose and VAR_AMPL_LICFILE not in os.environ:
        print(f'Found ampl.lic ("{ampl_lic}") but it is not writable.')
    if VAR_AMPLKEY_RUNTIME_DIR in os.environ:
        amplkey_dir = os.environ[VAR_AMPLKEY_RUNTIME_DIR]
    else:
        try:
            amplkey_dir = os.path.join(os.path.expanduser("~"), ".amplkey")
            if not os.path.isdir(amplkey_dir):
                os.makedirs(amplkey_dir)
        except:
            amplkey_dir = os.path.join(tempfile.gettempdir(), ".amplkey")
            if not os.path.isdir(amplkey_dir):
                os.makedirs(amplkey_dir)

    if VAR_AMPL_LICFILE not in os.environ:
        ampl_lic = os.path.join(amplkey_dir, "ampl.lic")
        if not os.path.isfile(ampl_lic):
            open(ampl_lic, "w").write(open(base_ampl_lic, "r").read())
        set_ampl_lic(ampl_lic)
    if VAR_AMPLKEY_RUNTIME_DIR not in os.environ:
        set_amplkey_runtime(amplkey_dir)


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
    for path in os.environ.get("PATH", "").split(os.pathsep):
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

    _prepare_amplkey_env()

    # Add all modules to ampl_libpath (necessary for plugins)
    ampl_libpath = os.environ.get("ampl_libpath", "").split("\n")
    for path in path_modules:
        if path not in ampl_libpath:
            ampl_libpath.append(path)
    if ampl_libpath:
        ampl_libpath = [path for path in ampl_libpath if path]
        os.environ["ampl_libpath"] = "\n".join(ampl_libpath)


def unload_modules(modules=[]):
    """
    Unload AMPL modules.
    Args:
        modules: list of modules to be unloaded.
    """
    modules = _sort_modules_for_loading(modules, add_base=False)
    to_remove = tuple(
        path[path.find("ampl_module_") :] for path in _locate_modules(modules)
    )
    os.environ["PATH"] = os.pathsep.join(
        [
            path
            for path in os.environ.get("PATH", "").split(os.pathsep)
            if not path.endswith(to_remove)
        ]
    )


def preload_modules(silently=True, verbose=False):
    """
    Load all modules to the end of environment variable PATH.
    Args:
        silently: ignore any errors and just return False
        verbose: show verbose output if True.
    """
    try:
        # head = False if _find_ampl_lic() else True
        load_modules(head=True, verbose=verbose)
        return True
    except:
        if not silently:
            raise
        return False


def path(modules=[], add_base=True):
    """
    Return PATH for AMPL modules.
    Args:
        modules: list of modules to be included.
    """
    modules = _sort_modules_for_loading(modules, add_base=add_base)
    return os.pathsep.join(_locate_modules(modules, verbose=False))


def find(filename):
    """
    Find a file in AMPL modules.
    Args:
        filename: name of the file to locate.
    """
    paths = path().split(os.pathsep)
    for p in paths:
        full_path = os.path.join(p, filename)
        if os.path.isfile(full_path):
            return full_path
        full_path = os.path.join(p, filename + ".exe")
        if os.path.isfile(full_path):
            return full_path
    raise FileNotFoundError(f"Could not find {filename} in any AMPL module.")


def _activate_default_license(platform, retry=3):
    from subprocess import getoutput
    from requests import post
    from time import sleep
    from json import loads
    from tempfile import mktemp, mkdtemp

    url = "https://portal.ampl.com/v1/amplkey"
    cmd = find("leasefingerprint") + " -s"
    fp = getoutput(cmd)
    for i in range(1, retry + 1):
        response = post(url, data={"uuid": platform, "fingerprint": fp})
        if response.status_code == 200:
            break
        elif i < retry:
            print("Default license activation failed. Retrying...")
            sleep(i)
        else:
            raise Exception("Failed to retrieve default license")
    tmpfile = mktemp(".lic")
    open(tmpfile, "w").write(loads(response.text)["license"])
    os.environ["AMPL_LICFILE"] = tmpfile
    os.environ["AMPL_LICFILE_DEFAULT"] = tmpfile
    os.environ["AMPLKEY_RUNTIME_DIR"] = mkdtemp()


def _handle_default_uuid():
    if "AMPL_LICFILE" in os.environ:
        return os.environ.get("AMPL_LICFILE", "") == os.environ.get(
            "AMPL_LICFILE_DEFAULT", ""
        )
    if cloud_platform_name() != "colab":
        return False
    try:
        _activate_default_license("colab")
        return True
    except:
        print("Failed to activate default license.")
        return False


def activate_license(uuid, verbose=False):
    """
    Activate an AMPL license using the UUID.
    Args:
        uuid: license uuid.
        verbose: show verbose output if True.
    """
    load_modules()
    if not isinstance(uuid, str):
        raise Exception("The license UUID must be a string.")
    if uuid == "default" or "license-uuid" in uuid:
        if _handle_default_uuid():
            return True
        else:
            print(
                "Please provide a valid license UUID. "
                "You can use free https://ampl.com/ce or https://ampl.com/courses licenses."
            )
            raise Exception(
                "Invalid license UUID. "
                "You can use free https://ampl.com/ce or https://ampl.com/courses licenses."
            )
    exit_code = run_command(
        ["amplkey", "activate", "--uuid", uuid],
        verbose=verbose,
    )
    if exit_code != 0:
        raise Exception("The license activation failed.")
    return True
