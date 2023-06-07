#!/bin/bash
cd "`dirname "$0"`"

cd swig
# -debug-symbols -builtin
swig -python -c++ -builtin -o ../../amplpy/amplpython/cppinterface/amplpythonPYTHON_wrap.cxx \
    -I../../amplpy/amplpython/cppinterface/include \
    python/amplpython.i
sed -i~ 's/class runtime_error(object):/class runtime_error(Exception):/' ../../amplpy/amplpython/cppinterface/amplpython.py
