# -*- coding: utf-8 -*-
__version__ = "0.4.0"

from .amplpypi import (
    add_to_path,
    install_modules,
    uninstall_modules,
    load_modules,
    installed_modules,
    available_modules,
)

from .commands import main

install = install_modules
uninstall = uninstall_modules
load = load_modules
installed = installed_modules
available = available_modules
