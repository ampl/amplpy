# -*- coding: utf-8 -*-
__version__ = "0.7.5"
from .notebooks import (
    ampl_notebook,
)

from .modules import (
    activate as activate_license,
    cloud_platform_name,
)

from .utils import (
    register_magics,
    add_to_path,
)

_SUPPORT_MESSAGE = """

For support/feedback go to https://discuss.ampl.com or e-mail <support@ampl.com>
"""

try:
    from IPython import get_ipython

    register_magics(ampl_object="ampl", globals_=get_ipython().user_global_ns)
except:
    pass
