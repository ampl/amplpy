# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import tempfile
import zipfile
import tarfile
import shutil
import os


def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def move(src, dst, verbose=False):
    target = os.path.join(dst, os.path.basename(src))
    if os.path.exists(target):
        if verbose:
            print('> {} (replacing)'.format(target))
        remove(target)
    elif verbose:
        print('> {} (new)'.format(target))
    shutil.move(src, dst)


def move_contents(src, dst, verbose=False):
    for fname in os.listdir(src):
        move(os.path.join(src, fname), dst, verbose)


def module_installer(url, destination, verbose=False):
    """Installs AMPL modules."""
    dst_basename = os.path.basename(destination)
    if not dst_basename.startswith('ampl.'):
        raise Exception(
            'Invalid destination. Must be a ampl.platform directory')

    tmpfile = tempfile.mktemp('.zip')
    tmpdir = tempfile.mkdtemp('ampl_tmp')

    def cleanup():
        for path in [tmpdir, tmpfile]:
            try:
                remove(path)
            except:
                pass

    try:
        print("Downloading:", url)
        urlretrieve(url, tmpfile)
        if url.endswith('.lic'):
            shutil.move(tmpfile, os.path.join(tmpdir, os.path.basename(url)))
        elif url.endswith('.zip'):
            with zipfile.ZipFile(tmpfile) as zp:
                zp.extractall(tmpdir)
        elif url.endswith(('.tgz', 'tar.gz')):
            with tarfile.open(tmpfile) as tarf:
                tarf.extractall(tmpdir)
        else:
            raise Exception('Invalid URL')
        try:
            os.remove(tmpfile)
        except:
            pass

        lst = os.listdir(tmpdir)
        if len(lst) != 1 or lst[0].startswith('ampl.') is False:
            raise Exception(
                'Invalid bundle contents. Expected ampl.platform directory')

        if os.path.exists(destination):
            if not os.path.isdir(destination):
                raise Exception('Invalid destination. Must be a directory')
        else:
            os.makedirs(destination)

        if lst[0] == 'ampl.lic':
            source = tmpdir
        elif lst[0] == dst_basename:
            source = os.path.join(tmpdir, lst[0])
        else:
            raise Exception(
                'Invalid destination for downloaded bundle ({} != {})'.format(
                    dst_basename, lst[0]
                ))

        move_contents(source, destination, verbose)
        cleanup()
    except:
        cleanup()
        raise


def ampl_installer(ampl_dir, modules=None, license_uuid=None, run_once=True, verbose=False):
    """Installs AMPL bundle or individual modules."""
    demo_lic_backup = os.path.join(ampl_dir, 'ampl.lic_demo')
    if run_once and os.path.isfile(demo_lic_backup):
        print('Already installed. Skipping.')
    elif modules is not None:
        for module in modules:
            module_installer(f'https://portal.ampl.com/dl/modules/{module}-module.linux64.tgz',
                             ampl_dir, verbose=verbose)
        shutil.copy(os.path.join(ampl_dir, 'ampl.lic'), demo_lic_backup)
    else:
        module_installer('https://portal.ampl.com/dl/amplce/ampl.linux64.tgz',
                         ampl_dir, verbose=verbose)
        shutil.copy(os.path.join(ampl_dir, 'ampl.lic'), demo_lic_backup)
    if license_uuid is not None:
        print(f'Activating license {license_uuid}')
        module_installer(f'https://portal.ampl.com/download/license/{license_uuid}/ampl.lic',
                         ampl_dir, verbose=verbose)
    else:
        print('Activating demo license.')
        shutil.copy(demo_lic_backup, os.path.join(ampl_dir, 'ampl.lic'))
    return ampl_dir


def cloud_platform_name():
    """Guesses the name of cloud platform currently running on."""
    import os
    envkeys = dict(os.environ).keys()
    if any(key.startswith('COLAB_') for key in envkeys):
        return 'colab'
    if any(key.startswith('KAGGLE_') for key in envkeys):
        return 'kaggle'
    if any(key.startswith('PAPERSPACE_') for key in envkeys):
        return 'paperspace'
    if 'SM_CURRENT_HOST' in envkeys:
        return 'sagemaker'
    return None
