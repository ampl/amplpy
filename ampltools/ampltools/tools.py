# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import subprocess
import tempfile
import zipfile
import tarfile
import shutil
import os


def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def move(src, dst, verbose=False):
    target = os.path.join(dst, os.path.basename(src))
    if os.path.exists(target):
        if verbose:
            print("> {} (replacing)".format(target))
        remove(target)
    elif verbose:
        print("> {} (new)".format(target))
    shutil.move(src, dst)


def move_contents(src, dst, verbose=False):
    for fname in os.listdir(src):
        move(os.path.join(src, fname), dst, verbose)


def module_installer(url, destination, verbose=False):
    """Installs AMPL modules."""
    dst_basename = os.path.basename(destination)
    if not dst_basename.startswith("ampl."):
        raise Exception("Invalid destination. Must be a ampl.platform directory")

    tmpfile = tempfile.mktemp(".zip")
    tmpdir = tempfile.mkdtemp("ampl_tmp")

    def cleanup():
        for path in [tmpdir, tmpfile]:
            try:
                remove(path)
            except:
                pass

    try:
        print("Downloading:", url)
        urlretrieve(url, tmpfile)
        if url.endswith(".zip"):
            with zipfile.ZipFile(tmpfile) as zp:
                zp.extractall(tmpdir)
        elif url.endswith((".tgz", "tar.gz")):
            with tarfile.open(tmpfile) as tarf:
                tarf.extractall(tmpdir)
        else:
            raise Exception("Invalid URL")
        try:
            os.remove(tmpfile)
        except:
            pass

        lst = os.listdir(tmpdir)
        if len(lst) != 1 or lst[0].startswith("ampl.") is False:
            raise Exception("Invalid bundle contents. Expected ampl.platform directory")

        if os.path.exists(destination):
            if not os.path.isdir(destination):
                raise Exception("Invalid destination. Must be a directory")
        else:
            os.makedirs(destination)

        if lst[0] == dst_basename:
            source = os.path.join(tmpdir, lst[0])
        else:
            raise Exception(
                "Invalid destination for downloaded bundle ({} != {})".format(
                    dst_basename, lst[0]
                )
            )

        move_contents(source, destination, verbose)
        cleanup()
    except:
        cleanup()
        raise


def activate_ampl_license(uuid):
    uuid = uuid.strip()
    url = "https://portal.ampl.com/download/license/{}/ampl.lic".format(uuid)
    tmpfile = tempfile.mktemp(".lic")
    urlretrieve(url, tmpfile)
    os.environ["AMPL_LICFILE"] = tmpfile


def ampl_installer(
    ampl_dir, modules=None, license_uuid=None, reinstall=False, verbose=False
):
    """Installs AMPL bundle or individual modules."""
    ampl_lic = os.path.join(ampl_dir, "ampl.lic")
    if reinstall is False and os.path.isfile(ampl_lic):
        print(
            "Already installed. Skipping. Set reinstall=True if you want to reinstall."
        )
    elif modules is not None:
        if "ampl" not in modules:
            modules.insert(0, "ampl")
        for module in modules:
            module_installer(
                "https://portal.ampl.com/dl/modules/{}-module.linux64.tgz".format(
                    module
                ),
                ampl_dir,
                verbose=verbose,
            )
    else:
        module_installer(
            "https://portal.ampl.com/dl/amplce/ampl.linux64.tgz",
            ampl_dir,
            verbose=verbose,
        )
    if license_uuid is not None:
        print("Activating license.")
        try:
            activate_ampl_license(license_uuid)
            print("License activated.")
        except:
            print("Failed to activate license.")
    return ampl_dir


def cloud_platform_name():
    """Guesses the name of cloud platform currently running on."""
    import os
    envkeys = dict(os.environ).keys()
    if any(key.startswith("COLAB_") for key in envkeys):
        return "colab"
    if os.path.isdir("/content/"):
        return "colab"
    if any(key.startswith("KAGGLE_") for key in envkeys):
        return "kaggle"
    if any(key.startswith("PAPERSPACE_") for key in envkeys):
        return "paperspace"
    if os.path.isdir("/home/studio-lab-user"):
        return "sagemaker-studio-lab"
    return None


def check_ampl_version():
    try:
        print(subprocess.getoutput("ampl -vvq"))
    except:
        print('Failed to invoke "ampl -vvq".')


def ampl_license_cell(check_callback):
    import ipywidgets as widgets
    from IPython.display import display

    print("AMPL License:")
    message = widgets.Output()
    version = widgets.Output()
    with message:
        ampl_lic = os.environ.get("AMPL_LICFILE", None)
        if ampl_lic is not None:
            print("License license at {}.".format(ampl_lic))
        else:
            print("Using demo license.")
    with version:
        if check_callback:
            print()
            check_callback()

    demo_btn = widgets.Button(description="Use demo license")
    uuid_input = widgets.Text(description="UUID:")

    def activate(where):
        uuid = uuid_input.value.strip()
        if where == "uuid" and len(uuid) == 0:
            return
        message.clear_output(wait=False)
        with message:
            if where == "demo":
                print("Activate demo license.")
                if "AMPL_LICFILE" in os.environ:
                    del os.environ["AMPL_LICFILE"]
            elif where == "uuid":
                if len(uuid) == 36:
                    uuid_input.value = ""  # clear the input
                    try:
                        activate_ampl_license(uuid)
                        print("License activated.")
                    except:
                        print("Failed to activate license.")
                        if "AMPL_LICFILE" in os.environ:
                            del os.environ["AMPL_LICFILE"]
                else:
                    print("Please provide a license UUID or use a demo license.")
                    return

        version.clear_output(wait=False)
        with version:
            if check_callback:
                print()
                check_callback()

    demo_btn.on_click(lambda b: activate("demo"), False)
    uuid_input.observe(lambda d: activate("uuid"), "value")
    display(widgets.VBox([widgets.HBox([demo_btn, uuid_input]), message, version]))


def ampl_installer_cell(
    license_uuid=None, modules=None, reinstall=False, check_callback=None
):
    if cloud_platform_name() is not None:
        ampl_dir = os.path.abspath(os.path.join(os.curdir, "ampl.linux-intel64"))
        ampl_installer(
            ampl_dir,
            modules=modules,
            license_uuid=license_uuid,
            reinstall=reinstall,
            verbose=True,
        )
        os.environ["PATH"] = ampl_dir + os.pathsep + os.environ["PATH"]
    else:
        print("Not running in a known cloud environment. Skipping installation.")
    if license_uuid is None:
        ampl_license_cell(check_callback=check_callback)
    else:
        print()
        if check_callback:
            check_callback()
        else:
            check_ampl_version()


def ampl_notebook(
    license_uuid=None,
    modules=None,
    reinstall=False,
    register_magics=True,
    globals_=None,
):
    if globals_ is None:
        globals_ = {}

    def instantiate_ampl():
        from amplpy import AMPL

        ampl = AMPL()
        print(ampl.option["version"])
        globals_["ampl"] = ampl

    ampl_installer_cell(
        license_uuid, modules, reinstall, check_callback=instantiate_ampl
    )
    if register_magics:
        register_magics_global(ampl_object="ampl", globals_=globals_)
    return globals_.get("ampl", None)


def register_magics_global(store_name="_ampl_cells", ampl_object=None, globals_=None):
    """
    Register jupyter notebook magics ``%%ampl`` and ``%%ampl_eval``.
    Args:
        store_name: Name of the store where ``%%ampl cells`` will be stored.
        ampl_object: Object used to evaluate ``%%ampl_eval`` cells.
    """
    from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
    from IPython import get_ipython

    @magics_class
    class StoreAMPL(Magics):
        def __init__(self, shell=None, **kwargs):
            Magics.__init__(self, shell=shell, **kwargs)
            self._store = []
            shell.user_ns[store_name] = self._store

        @cell_magic
        def ampl(self, line, cell):
            """Store the cell in the store"""
            self._store.append(cell)

        @cell_magic
        def ampl_eval(self, line, cell):
            """Evaluate the cell"""
            if globals_ is not None:
                if isinstance(ampl_object, str):
                    ampl = globals_[ampl_object]
                else:
                    ampl = ampl_object
            ampl.eval(cell)

        @line_magic
        def get_ampl(self, line):
            """Retrieve the store"""
            return self._store

    get_ipython().register_magics(StoreAMPL)
