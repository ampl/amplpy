# -*- coding: utf-8 -*-
import subprocess
import os
from .licenses import is_valid_uuid, activate_license, _activate_default_license
from .pymodules import install_modules, load_modules
from .utils import cloud_platform_name


def _deactivate_license():
    if "AMPL_LICFILE_DEFAULT" in os.environ:
        os.environ["AMPL_LICFILE"] = os.environ["AMPL_LICFILE_DEFAULT"]
    elif "AMPL_LICFILE" in os.environ:
        del os.environ["AMPL_LICFILE"]


def _ampl_license_cell(check_callback):
    import ipywidgets as widgets
    from IPython.display import display

    platform = cloud_platform_name()
    if platform is not None:
        print("AMPL License UUID (you can use a free https://ampl.com/ce license):")
    else:
        print("AMPL License UUID:")
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

    def activate(where):
        uuid = uuid_input.value.strip()
        if where == "uuid" and len(uuid) == 0:
            return
        message.clear_output(wait=False)
        with message:
            if where == "existing":
                print("Switch to existing license.")
                _deactivate_license()
            elif where == "uuid":
                if len(uuid) == 36:
                    uuid_input.value = ""  # clear the input
                    try:
                        activate_license(uuid)
                        print("License activated.")
                    except:
                        print("Failed to activate license.")
                        _deactivate_license()
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


def _handle_default_uuid():
    if "AMPL_LICFILE" not in os.environ and cloud_platform_name() == "colab":
        try:
            from ampl_module_base import bin_dir

            _activate_default_license(bin_dir, "colab")
        except:
            print("Failed to activate default license.")


def ampl_notebook(
    modules=None,
    license_uuid=None,
    reinstall=False,
    globals_=None,
    verbose=False,
    register_magics=True,
    show_license=None,
):
    show_prompt = globals_ is not None
    if show_license is None:
        show_license = show_prompt
    if globals_ is None:
        globals_ = {}

    def instantiate_ampl(print_license=True):
        from amplpy import AMPL, Environment

        if cloud_platform_name() == "colab":
            try:
                ampl = AMPL(Environment("", "x-ampl"))
                ampl.option["show_context"] = 1
            except Exception:
                print("Failed to start x-ampl session. Using regular ampl instead.")
                ampl = AMPL()
        else:
            ampl = AMPL()
        if print_license:
            version = ampl.option["version"]
            for row in version.split("\n"):
                if row.startswith("Licensed to "):
                    print(row)
                    break
            else:
                print(version)
        globals_["ampl"] = ampl

    install_modules(modules, reinstall=reinstall, verbose=verbose)
    load_modules(modules, verbose=verbose)

    if license_uuid is None or license_uuid == "default":
        _handle_default_uuid()

    if license_uuid == "default":
        instantiate_ampl(print_license=show_license)
    elif not is_valid_uuid(license_uuid):
        if license_uuid not in (None, ""):
            print(
                "Please provide a valid license UUID. "
                "You can use a free https://ampl.com/ce license."
            )
            _deactivate_license()
        if show_prompt:
            _ampl_license_cell(check_callback=instantiate_ampl)
        else:
            instantiate_ampl(print_license=True)
    else:
        try:
            activate_license(license_uuid)
            instantiate_ampl(print_license=show_license)
        except:
            print("Failed to activate license.")
            _deactivate_license()
            if show_prompt:
                _ampl_license_cell(check_callback=instantiate_ampl)
            else:
                instantiate_ampl(print_license=True)

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
            ampl.eval("\n" + cell)

        @line_magic
        def get_ampl(self, line):
            """Retrieve the store"""
            return self._store

    get_ipython().register_magics(StoreAMPL)
