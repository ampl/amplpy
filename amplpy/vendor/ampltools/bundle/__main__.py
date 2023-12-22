#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

USAGE = """Usage:
    $ python -m $PACKAGE.bundle script.py <extra arguments>
"""


def bundle(args):
    if len(args) < 2 or not args[1].endswith(".py"):
        print(
            USAGE.replace("$PACKAGE", "amplpy" if "amplpy" in args[0] else "ampltools")
        )
        sys.exit(1)

    from amplpy import modules, __file__ as amplpy_dir

    main_script = args[1]
    extra_arguments = args[2:]

    try:
        shutil.rmtree("dist")
    except:
        pass

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
            "--copy-metadata",
            "--collect-submodules",
            "--collect-datas",
            "--collect-binaries",
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

    if exit_code == 0:
        # Locate the executable
        basename = os.path.basename(main_script).replace(".py", "")
        executable = os.path.join(
            os.path.abspath(os.curdir), "dist", basename, basename
        )
        if not os.path.exists(executable):
            executable += ".exe"
        if os.path.exists(executable):
            print(f'\n\nYour executable is at "{executable}".')

    sys.exit(exit_code)


if __name__ == "__main__":
    bundle(sys.argv)
