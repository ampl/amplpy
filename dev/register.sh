#!/bin/bash
cd "`dirname "$0"`"
cd ..
set -ex

bash clear.sh
rm -rf dist/*
rm -rf build *.egg-info

#python setup.py register
#python setup.py build
python setup.py sdist #bdist_wheel
twine upload dist/*.tar.gz
#python setup.py sdist bdist_wheel upload
