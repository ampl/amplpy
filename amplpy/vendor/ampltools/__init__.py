# -*- coding: utf-8 -*-
__version__ = "0.5.2"
from .notebooks import (
    ampl_notebook,
)

from .modules import (
    activate as activate_license,
)

from .utils import (
    cloud_platform_name,
    register_magics,
    add_to_path,
)

_SUPPORT_MESSAGE = """

Please report any bugs at: https://github.com/ampl/amplpy

For support/feedback go to https://discuss.ampl.com or e-mail <support@ampl.com>
"""