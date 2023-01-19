# -*- coding: utf-8 -*-
__version__ = "0.4.0"

from .amplpypi import (
    add_to_path,
    install_modules as install,
    uninstall_modules as uninstall,
    load_modules as load,
    installed_modules as installed,
    available_modules as available,
)

from .commands import _main
