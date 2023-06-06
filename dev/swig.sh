#!/bin/bash
cd "`dirname "$0"`"

cd swig
# -debug-symbols
swig -python -c++ -builtin -o ../../amplpy/amplpython/cppinterface/amplpythonPYTHON_wrap.cxx \
    -I../../amplpy/amplpython/cppinterface/include \
    python/amplpython.i
