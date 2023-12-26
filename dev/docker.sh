#!/bin/bash
cd "`dirname "$0"`"
cd ..
set -ex

PREFIX="fdabrandao/manylinux:"
SUFFIX=""
OPTIONS="-v `pwd`:/shared -it --rm"

if [ "$#" -ne 1 ]; then
  	echo "Usage: $0 <arch>"
else
    ARCH=$1
    docker run $OPTIONS ${PREFIX}${ARCH}${SUFFIX} bash
fi
