#!/bin/bash
cd `dirname $0`

docker pull quay.io/pypa/manylinux1_i686
docker pull quay.io/pypa/manylinux1_x86_64

docker rm manylinux32 manylinux32_tmp
docker run -v `pwd`:/manylinux -it --name manylinux32_tmp quay.io/pypa/manylinux1_i686 /manylinux/bootstrap.sh 32 || exit 1
docker commit manylinux32_tmp manylinux32
docker rm manylinux32_tmp

docker rm manylinux64 manylinux64_tmp
docker run -v `pwd`:/manylinux -it --name manylinux64_tmp quay.io/pypa/manylinux1_x86_64 /manylinux/bootstrap.sh 64 || exit 1
docker commit manylinux64_tmp manylinux64
docker rm manylinux64_tmp

