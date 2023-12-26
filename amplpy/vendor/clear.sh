#!/bin/bash
cd "`dirname "$0"`"
set -ex

find ./ -name "*~" -exec rm -v "{}" \; 2>/dev/null
find ./ -name "*.pyc" -exec rm -v "{}" \; 2>/dev/null
find ./ -name "*.pyo" -exec rm -v "{}" \; 2>/dev/null
find ./ -name "*.o" -exec rm -v "{}" \; 2>/dev/null
find ./ -name "__pycache__" -exec rm -rf "{}" \; 2>/dev/null

rm -rf src/.deps/
rm -f src/stamp-h1
rm -f src/.dirstamp
rm -f config.status
rm -rf autom4te.cache/
rm -f Makefile
rm -f config.log
rm -rf *.egg-info

rm -rf build
rm -rf dist
