# -*- coding: utf-8 -*-
import os
from .modules import activate as activate_license
from .modules import install as install_modules
from .modules import load as load_modules
from .modules import cloud_platform_name
from .utils import (
    register_magics,
    _is_valid_uuid,
)


def _deactivate_license():
    if "AMPL_LICFILE_DEFAULT" in os.environ:
        os.environ["AMPL_LICFILE"] = os.environ["AMPL_LICFILE_DEFAULT"]
    elif "AMPL_LICFILE" in os.environ:
        del os.environ["AMPL_LICFILE"]


def _ampl_license_cell(check_callback):
    try:
        import ipywidgets as widgets
    except ImportError:
        check_callback()
        return
    from IPython.display import display

    header = widgets.Output()
    message = widgets.Output()
    version = widgets.Output()

    platform = cloud_platform_name()
    with header:
        print(
            "AMPL License UUID (you can use free https://ampl.com/ce or https://ampl.com/courses licenses):"
        )
    with message:
        ampl_lic = os.environ.get("AMPL_LICFILE", None)
        if ampl_lic is not None and platform is None:
            print(f"License license at {ampl_lic}.")
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


def ampl_notebook(
    modules=[],
    license_uuid=None,
    reinstall=False,
    verbose=False,
    show_license=None,
    **kwargs,
):
    try:
        from IPython import get_ipython
    except:
        get_ipython = lambda: None
    globals_ = kwargs.get("globals_", kwargs.get("g", None))
    if globals_ is None:
        if get_ipython() is not None:
            globals_ = get_ipython().user_global_ns
        else:
            globals_ = {}

    show_prompt = get_ipython() is not None and globals_ is not None
    if show_license is None:
        show_license = True

    def instantiate_ampl(print_license=True):
        from amplpy import AMPL

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
    else:
        modules = []

    open_modules = [
        "highs",
        "cbc",
        "couenne",
        "bonmin",
        "ipopt",
        "coin",
        "gcg",
        "scip",
        "gecode",
        "open",
        "plugins",
        "ampl",
    ]
    open_source_only = len(set(modules) - set(open_modules)) == 0

    using_default_license = license_uuid is not None and (
        license_uuid == "default" or "license-uuid" in license_uuid
    )

    # Ignore default license outside colab
    if using_default_license and cloud_platform_name() != "colab":
        using_default_license = False
        license_uuid = None

    if using_default_license:
        using_default_license = activate_license("default")
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

    if get_ipython() is not None:
        register_magics(ampl_object="ampl", globals_=globals_)
    return globals_.get("ampl", None)
