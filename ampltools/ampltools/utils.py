# -*- coding: utf-8 -*-
import platform
import os
from uuid import UUID


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


def _is_valid_uuid(uuid):
    if uuid in (None, ""):
        return False
    try:
        UUID(str(uuid))
    except ValueError:
        return False

    return True
