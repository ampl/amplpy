# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import subprocess
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
        if url.endswith('.zip'):
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

        if lst[0] == dst_basename:
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


def activate_ampl_license(uuid):
    url = f'https://portal.ampl.com/download/license/{uuid}/ampl.lic'
    tmpfile = tempfile.mktemp('.lic')
    urlretrieve(url, tmpfile)
    os.environ["AMPL_LICFILE"] = tmpfile


def ampl_installer(ampl_dir, modules=None, license_uuid=None, run_once=True, verbose=False):
    """Installs AMPL bundle or individual modules."""
    ampl_lic = os.path.join(ampl_dir, 'ampl.lic')
    if run_once and os.path.isfile(ampl_lic):
        print(
            'Already installed. Skipping. Set run_once=False if you want to install again.')
    elif modules is not None:
        if 'ampl' not in modules:
            modules.append('ampl')
        for module in modules:
            module_installer(
                f'https://portal.ampl.com/dl/modules/{module}-module.linux64.tgz',
                ampl_dir, verbose=verbose)
    else:
        module_installer('https://portal.ampl.com/dl/amplce/ampl.linux64.tgz',
                         ampl_dir, verbose=verbose)
    if license_uuid is not None:
        print('Activating license.')
        try:
            activate_ampl_license(license_uuid)
            print('License activated.')
        except:
            print('Failed to activate license.')
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
    if os.path.isdir('/home/studio-lab-user'):
        return 'sagemaker-studio-lab'
    return None


def ampl_license_cell():
    import ipywidgets as widgets
    from IPython.display import display

    out = widgets.Output()
    with out:
        ampl_lic = os.environ.get('AMPL_LICFILE', None)
        if ampl_lic is not None:
            print(f'License license at {ampl_lic}.')
        else:
            print('Using demo license.')
    demo_btn = widgets.Button(description='Use demo license')
    activate_btn = widgets.Button(description='Activate')
    uuid_input = widgets.Password(description='UUID:')

    def activate(btn):
        uuid = uuid_input.value
        out.clear_output(wait=False)
        with out:
            if btn == demo_btn:
                print('Activate demo license.')
                if 'AMPL_LICFILE' in os.environ:
                    del os.environ['AMPL_LICFILE']
            else:
                if uuid != '':
                    try:
                        activate_ampl_license(uuid)
                        print('License activated.')
                    except:
                        print('Failed to activate license.')
                        if 'AMPL_LICFILE' in os.environ:
                            del os.environ['AMPL_LICFILE']
                else:
                    print('Please provide the license UUID or use a demo license.')
            try:
                print('\n' + subprocess.getoutput("ampl -vvq"))
            except:
                pass

    demo_btn.on_click(activate, False)
    activate_btn.on_click(activate, False)
    display(widgets.VBox(
        [widgets.HBox([demo_btn, uuid_input, activate_btn]), out]))


def ampl_installer_cell(license_uuid=None, modules=None, run_once=True):
    if cloud_platform_name() is not None:
        ampl_dir = os.path.abspath(
            os.path.join(os.curdir, 'ampl.linux-intel64'))
        ampl_installer(ampl_dir, modules=modules,
                       license_uuid=license_uuid, run_once=run_once, verbose=True)
        os.environ['PATH'] += os.pathsep + ampl_dir
    else:
        print('Not running in a known cloud platform. Skipping.')
    if license_uuid is None:
        ampl_license_cell()
    else:
        try:
            print('\n' + subprocess.getoutput("ampl -vvq"))
        except:
            pass
