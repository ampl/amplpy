# -*- coding: utf-8 -*-
import platform
import subprocess
import tempfile
import requests
import json
import time
import os
from uuid import UUID


def _is_valid_uuid(uuid):
    if uuid in (None, ""):
        return False
    try:
        UUID(str(uuid))
    except ValueError:
        return False

    return True


def _activate_default_license(ampl_dir, platform, retry=3):
    url = "https://portal.ampl.com/v1/amplkey"
    cmd = os.path.join(ampl_dir, "leasefingerprint") + " -s"
    fp = subprocess.getoutput(cmd)
    for i in range(1, retry + 1):
        response = requests.post(url, data={"uuid": platform, "fingerprint": fp})
        if response.status_code == 200:
            break
        elif i < retry:
            print("Default license activation failed. Retrying...")
            time.sleep(i)
        else:
            raise Exception("Failed to retrieve default license")
    tmpfile = tempfile.mktemp(".lic")
    open(tmpfile, "w").write(json.loads(response.text)["license"])
    os.environ["AMPL_LICFILE"] = tmpfile
    os.environ["AMPL_LICFILE_DEFAULT"] = tmpfile
    os.environ["AMPLKEY_RUNTIME_DIR"] = tempfile.mkdtemp()


def add_to_path(path, head=True):
    if head:
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    else:
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + path


def cloud_platform_name():
    """Guesses the name of cloud platform currently running on."""
    if platform.system() != "Linux":
        return None
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


def register_magics(store_name="_ampl_cells", ampl_object=None, globals_=None):
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
            if globals_ is not None and isinstance(ampl_object, str):
                ampl = globals_[ampl_object]
            else:
                ampl = ampl_object
            ampl.eval("\n" + cell)

        @line_magic
        def get_ampl(self, line):
            """Retrieve the store"""
            return self._store

    get_ipython().register_magics(StoreAMPL)
