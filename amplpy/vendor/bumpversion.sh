#!/bin/bash
cd "`dirname "$0"`"
set -ex

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <version>"
else
  version=$1
  sed -i~ "s/version=\"[^']*\"/version=\"$version\"/" setup.py
  sed -i~ "s/__version__ = \"[^']*\"/__version__ = \"$version\"/" ampltools/__init__.py
  sed -i~ "s/__version__ = \"[^']*\"/__version__ = \"$version\"/" ampltools/modules/__init__.py
  sed -i~ "s/ampltools[ ]*>=[ ]*[^\"]*\"/ampltools >= $version\"/" ../../setup.py
fi
