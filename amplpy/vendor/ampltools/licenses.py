# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import subprocess
import tempfile
import requests
import json
import time
import os
from .utils import _is_valid_uuid


def _activate_ampl_license(uuid, retry=3):
    if not _is_valid_uuid(uuid):
        raise ValueError("Invalid license UUID")
    uuid = uuid.strip()
    url = "https://portal.ampl.com/download/license/{}/ampl.lic".format(uuid)
    tmpfile = tempfile.mktemp(".lic")
    for i in range(1, retry + 1):
        try:
            urlretrieve(url, tmpfile)
        except Exception:
            if i < retry:
                print("License activation failed. Retrying...")
                time.sleep(i)
            else:
                raise
    os.environ["AMPL_LICFILE"] = tmpfile
    os.environ["AMPLKEY_RUNTIME_DIR"] = tempfile.mkdtemp()


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


def activate_license(license_uuid=None, verbose=False):
    """
    Activate AMPL license.
    Args:
        uuid: license UUID.
        verbose: show verbose output if True.
    """
    if not _is_valid_uuid(license_uuid):
        raise ValueError("Invalid license UUID.")

    if verbose:
        print("Activating license.")
    try:
        _activate_ampl_license(license_uuid)
        if verbose:
            print("License activated.")
        return True
    except Exception:
        raise RuntimeError("Failed to activate license.")
