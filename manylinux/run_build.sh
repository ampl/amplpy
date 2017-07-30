#!/bin/bash
cd `dirname $0`

rm -rf wheelhouse/*.whl
docker run -v `pwd`/..:/shared -it --rm manylinux32 /shared/manylinux/script_build.sh 32 || exit 1
docker run -v `pwd`/..:/shared -it --rm manylinux64 /shared/manylinux/script_build.sh 64 || exit 1

