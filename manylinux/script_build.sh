#!/bin/bash

set -e
BASE_PATH=$PATH
PYLIST="cp27-cp27m cp27-cp27mu cp33-cp33m cp34-cp34m cp35-cp35m cp36-cp36m"

if [ "$#" -eq 0 ]; then
  	echo "Usage: $0 [32|64]"
elif [ -d "/shared/manylinux/" ]; then
    cd ~
    cp -r /shared amplpy
    cd amplpy
    for pyversion in $PYLIST; do
        export PATH=/opt/python/$pyversion/bin/:$BASE_PATH
        echo $PATH
        rm -rf build dist
        python setup.py bdist_wheel
        auditwheel repair dist/*.whl
        mv wheelhouse/*.whl /shared/manylinux/wheelhouse
    done;
else
    echo "Must be run inside a docker container."
fi

