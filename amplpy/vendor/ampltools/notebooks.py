# -*- coding: utf-8 -*-
import os
from .modules import activate as activate_license
from .modules import install as install_modules
from .modules import load as load_modules
from .utils import (
    cloud_platform_name,
    register_magics,
    _is_valid_uuid,
    _activate_default_license,
)


def _deactivate_license():
    if "AMPL_LICFILE_DEFAULT" in os.environ:
        os.environ["AMPL_LICFILE"] = os.environ["AMPL_LICFILE_DEFAULT"]
    elif "AMPL_LICFILE" in os.environ:
        del os.environ["AMPL_LICFILE"]


def _ampl_license_cell(check_callback):
    import ipywidgets as widgets
    from IPython.display import display

    header = widgets.Output()
    message = widgets.Output()
    version = widgets.Output()

    platform = cloud_platform_name()
    with header:
        print("AMPL License UUID (you can use a free https://ampl.com/ce license):")
    with message:
        ampl_lic = os.environ.get("AMPL_LICFILE", None)
        if ampl_lic is not None and platform is None:
            print("License license at {}.".format(ampl_lic))
    with version:
        if check_callback:
            check_callback()

    uuid_input = widgets.Text(
        description="License UUID:", style={"description_width": "initial"}
    )

    def activate(where):
        uuid = uuid_input.value.strip()
        if where == "uuid" and len(uuid) == 0:
            return
        message.clear_output(wait=False)
        with message:
            if where == "uuid":
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

    uuid_input.observe(lambda d: activate("uuid"), "value")
    display(widgets.VBox([header, widgets.HBox([uuid_input]), message, version]))


def _handle_default_uuid():
    if "AMPL_LICFILE" in os.environ:
        return os.environ.get("AMPL_LICFILE", "") == os.environ.get(
            "AMPL_LICFILE_DEFAULT", ""
        )
    if cloud_platform_name() != "colab":
        return False
    try:
        from ampl_module_base import bin_dir

        _activate_default_license(bin_dir, "colab")
        return True
    except:
        print("Failed to activate default license.")
        return False


def ampl_notebook(
    modules=[],
    license_uuid=None,
    reinstall=False,
    verbose=False,
    show_license=None,
    **kwargs
):
    from IPython import get_ipython

    globals_ = kwargs.get("globals_", kwargs.get("g", None))
    if globals_ is None:
        globals_ = get_ipython().user_global_ns
    show_prompt = globals_ is not None
    if show_license is None:
        show_license = True

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

    if modules not in (None, []):
        install_modules(modules, reinstall=reinstall, verbose=verbose)
        load_modules(modules, verbose=verbose)
    else:
        modules = []

    using_default_license = license_uuid in (None, "", "default", "your-license-uuid")
    open_modules = [
        "highs",
        "cbc",
        "coin",
        "gecode",
        "scip",
        "gcg",
        "open",
        "plugins",
        "ampl",
    ]
    open_source_only = len(set(modules) - set(open_modules)) == 0

    if using_default_license:
        using_default_license = _handle_default_uuid()
    if using_default_license:
        if show_prompt and open_source_only:
            show_prompt = False
        if not show_prompt:
            print(
                "Using default Community Edition License for Colab. "
                "Get yours at: https://ampl.com/ce"
            )

    if using_default_license:
        if show_prompt:
            _ampl_license_cell(check_callback=instantiate_ampl)
        else:
            instantiate_ampl(print_license=show_license)
    elif not _is_valid_uuid(license_uuid):
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

    register_magics(ampl_object="ampl", globals_=globals_)
    return globals_.get("ampl", None)
