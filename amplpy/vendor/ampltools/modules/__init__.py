# -*- coding: utf-8 -*-
__version__ = "0.5.4"

from .amplpypi import (
    path,
    run_command as run,
    activate_license as activate,
    install_modules as install,
    uninstall_modules as uninstall,
    load_modules as load,
    unload_modules as unload,
    preload_modules as preload,
    installed_modules as installed,
    available_modules as available,
    generate_requirements as requirements,
)

from .commands import _main
