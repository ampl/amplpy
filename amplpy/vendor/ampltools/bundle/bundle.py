# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

USAGE = """Usage:
    $ python -m $PACKAGE.bundle script.py <extra arguments>
"""


def bundle(args):
    from amplpy import modules, __file__ as amplpy_dir

    main_script = args[0]
    extra_arguments = args[1:]
    basename = os.path.basename(main_script).replace(".py", "")
    dist_dir = os.path.join(os.path.abspath(os.curdir), "dist", basename)
    keep_license = "--keep-license" in extra_arguments
    if keep_license:
        extra_arguments.remove("--keep-license")

    if os.path.isdir(dist_dir):
        print(f"Deleting: {dist_dir}")
        shutil.rmtree(dist_dir)

    # List of modules and paths to include
    pymods = ["amplpy", "ampltools"] + [
        "ampl_module_" + mod for mod in modules.installed()
    ]
    paths = os.path.join(os.path.dirname(amplpy_dir), "amplpython", "cppinterface")

    # Build PyInstaller command
    cmd = [sys.executable, "-m", "PyInstaller", main_script]
    for pymod in pymods:
        for collect in [
            "--collect-all",
            # "--copy-metadata",
            # "--collect-submodules",
            # "--collect-datas",
            # "--collect-binaries",
        ]:
            cmd += [collect, pymod]
    cmd += ["--paths", paths]
    cmd += extra_arguments

    # Run the command
    print("$ " + " ".join(cmd))
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in process.stdout:
        print(line, end="")
    exit_code = process.wait()

    if not keep_license:
        for fname in ["ampl.lic", "amplkey.log"]:
            to_delete = os.path.join(
                dist_dir, "_internal", "ampl_module_base", "bin", fname
            )
            if os.path.isfile(to_delete):
                print(f"Deleting: {to_delete}")
                os.remove(to_delete)

    if exit_code == 0:
        # Locate the executable
        executable = os.path.join(dist_dir, basename)
        if not os.path.exists(executable):
            executable += ".exe"
        if os.path.exists(executable):
            print(f'\n\nYour executable is at "{executable}".')

    sys.exit(exit_code)


def _main():
    args = sys.argv
    if len(args) < 2 or not args[1].endswith(".py"):
        print(
            USAGE.replace("$PACKAGE", "amplpy" if "amplpy" in args[0] else "ampltools")
        )
        sys.exit(1)
    bundle(args[1:])
