#!/bin/bash
cd "`dirname "$0"`"
cd ..

cd swig
swig -python -c++ -builtin -o ../amplpy/amplpython/cppinterface/amplpythonPYTHON_wrap.cxx \
    -I../amplpy/amplpython/cppinterface/include \
    python/amplpython.i
