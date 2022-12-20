# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import tempfile
import zipfile
import tarfile
import shutil
import os
from .licenses import _activate_ampl_license, _activate_default_license
from .utils import cloud_platform_name


def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def move(src, dst, verbose=False):
    target = os.path.join(dst, os.path.basename(src))
    if os.path.exists(target):
        if verbose:
            print("> {} (replacing)".format(target))
        remove(target)
    elif verbose:
        print("> {} (new)".format(target))
    shutil.move(src, dst)


def move_contents(src, dst, verbose=False):
    for fname in os.listdir(src):
        move(os.path.join(src, fname), dst, verbose)


def _module_installer(url, destination, verbose=False):
    """Installs AMPL modules."""
    dst_basename = os.path.basename(destination)
    if not dst_basename.startswith("ampl."):
        raise Exception("Invalid destination. Must be a ampl.platform directory")

    tmpfile = tempfile.mktemp(".zip")
    tmpdir = tempfile.mkdtemp("ampl_tmp")

    def cleanup():
        for path in [tmpdir, tmpfile]:
            try:
                remove(path)
            except:
                pass

    try:
        print("Downloading:", url)
        urlretrieve(url, tmpfile)
        if url.endswith(".zip"):
            with zipfile.ZipFile(tmpfile) as zp:
                zp.extractall(tmpdir)
        elif url.endswith((".tgz", "tar.gz")):
            with tarfile.open(tmpfile) as tarf:
                tarf.extractall(tmpdir)
        else:
            raise Exception("Invalid URL")
        try:
            os.remove(tmpfile)
        except:
            pass

        lst = os.listdir(tmpdir)
        if len(lst) != 1 or lst[0].startswith("ampl.") is False:
            raise Exception("Invalid bundle contents. Expected ampl.platform directory")

        if os.path.exists(destination):
            if not os.path.isdir(destination):
                raise Exception("Invalid destination. Must be a directory")
        else:
            os.makedirs(destination)

        if lst[0] == dst_basename:
            source = os.path.join(tmpdir, lst[0])
        else:
            raise Exception(
                "Invalid destination for downloaded bundle ({} != {})".format(
                    dst_basename, lst[0]
                )
            )

        move_contents(source, destination, verbose)
        cleanup()
    except:
        cleanup()
        raise


def ampl_installer(
    ampl_dir, modules=None, license_uuid=None, reinstall=False, verbose=False
):
    """Installs AMPL bundle or individual modules."""
    ampl_lic = os.path.join(ampl_dir, "ampl.lic")
    if reinstall is False and os.path.isfile(ampl_lic):
        print(
            "Already installed. Skipping. Set reinstall=True if you want to reinstall."
        )
    elif modules is not None:
        if "ampl" not in modules:
            modules.insert(0, "ampl")
        for module in modules:
            _module_installer(
                "https://portal.ampl.com/dl/modules/{}-module.linux64.tgz".format(
                    module
                ),
                ampl_dir,
                verbose=verbose,
            )
    else:
        _module_installer(
            "https://portal.ampl.com/dl/amplce/ampl.linux64.tgz",
            ampl_dir,
            verbose=verbose,
        )
    if license_uuid is not None:
        print("Activating license.")
        try:
            _activate_ampl_license(license_uuid)
            print("License activated.")
        except:
            print("Failed to activate license.")
    elif cloud_platform_name() == "colab":
        print("Activating default license.")
        try:
            _activate_default_license(ampl_dir, "colab")
            print("Default license activated.")
        except:
            print("Failed to activate default license.")
    return ampl_dir
