#!/bin/bash

set -e
BASE_PATH=$PATH
PYLIST="cp27-cp27m cp27-cp27mu cp34-cp34m cp35-cp35m cp36-cp36m cp37-cp37m"

if [ "$#" -eq 0 ]; then
  	echo "Usage: $0 [32|64]"
elif [ -d "/shared/manylinux/" ]; then
    cd ~
    cp -r /shared amplpy
    cd amplpy
    for pyversion in $PYLIST; do
        export PATH=/opt/python/$pyversion/bin/:/opt/ampl.linux$1/:$BASE_PATH
        echo $PATH
        rm -rf build dist venv
        pip install virtualenv
        virtualenv venv
        source venv/bin/activate
        pip install . --upgrade
        python -m amplpy.tests || exit 1
        # python examples/test_examples.py || exit 1
        deactivate
    done;
else
    echo "Must be run inside a docker container."
fi
