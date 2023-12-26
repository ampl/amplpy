#!/bin/bash
cd "`dirname "$0"`"
cd ..
set -ex

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <version>"
else
  version=$1
  sed -i~ "s/amplpy==.*/amplpy==$version/" docs/requirements.txt
  sed -i~ "s/version=\"[^\"]*\"/version=\"$version\"/" setup.py
  sed -i~ "s/__version__ = \"[^\"]*\"/__version__ = \"$version\"/" amplpy/__init__.py
fi

