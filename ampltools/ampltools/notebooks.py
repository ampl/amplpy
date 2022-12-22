# -*- coding: utf-8 -*-
import subprocess
import os
from .licenses import _activate_ampl_license, _activate_default_license
from .pymodules import install_modules, load_modules
from .utils import cloud_platform_name


def ampl_license_cell(check_callback):
    import ipywidgets as widgets
    from IPython.display import display

    if "AMPL_LICFILE" not in os.environ and cloud_platform_name() == "colab":
        try:
            from ampl_module_base import bin_dir

            _activate_default_license(bin_dir, "colab")
        except:
            print("Failed to activate default license.")

    platform = cloud_platform_name()
    if platform is not None:
        print("AMPL License (you can use a free https://ampl.com/ce license):")
    else:
        print("AMPL License:")
    message = widgets.Output()
    version = widgets.Output()
    with message:
        ampl_lic = os.environ.get("AMPL_LICFILE", None)
        if ampl_lic is not None and platform is None:
            print("License license at {}.".format(ampl_lic))
    with version:
        if check_callback:
            check_callback()

    existing_btn = widgets.Button(description="Use existing license")
    uuid_input = widgets.Text(description="UUID:")

    def deactivate():
        if "AMPL_LICFILE_DEFAULT" in os.environ:
            os.environ["AMPL_LICFILE"] = os.environ["AMPL_LICFILE_DEFAULT"]
        elif "AMPL_LICFILE" in os.environ:
            del os.environ["AMPL_LICFILE"]

    def activate(where):
        uuid = uuid_input.value.strip()
        if where == "uuid" and len(uuid) == 0:
            return
        message.clear_output(wait=False)
        with message:
            if where == "existing":
                print("Switch to existing license.")
                deactivate()
            elif where == "uuid":
                if len(uuid) == 36:
                    uuid_input.value = ""  # clear the input
                    try:
                        _activate_ampl_license(uuid)
                        print("License activated.")
                    except:
                        print("Failed to activate license.")
                        deactivate()
                else:
                    print("Please provide a license UUID or use an existing license.")
                    return

        version.clear_output(wait=False)
        with version:
            if check_callback:
                check_callback()

    existing_btn.on_click(lambda b: activate("existing"), False)
    uuid_input.observe(lambda d: activate("uuid"), "value")
    display(widgets.VBox([widgets.HBox([existing_btn, uuid_input]), message, version]))


def ampl_notebook(
    license_uuid=None,
    modules=None,
    reinstall=False,
    register_magics=True,
    globals_=None,
    verbose=False,
):
    if globals_ is None:
        globals_ = {}

    def instantiate_ampl():
        from amplpy import AMPL

        ampl = AMPL()
        version = ampl.option["version"]
        for row in version.split("\n"):
            if row.startswith("Licensed to "):
                print(row)
                break
        else:
            print(version)
        globals_["ampl"] = ampl

    install_modules(modules, reinstall=reinstall, verbose=verbose)
    load_modules(verbose=verbose)
    if license_uuid is None:
        ampl_license_cell(check_callback=instantiate_ampl)
    else:
        instantiate_ampl()

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
