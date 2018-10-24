#!/bin/bash

if [ "$#" -eq 0 ]; then
  	echo "Usage: $0 [32|64]"
else
    cd /tmp/
    curl -O https://cmake.org/files/v3.12/cmake-3.12.3.tar.gz
    tar xzvf cmake-3.12.3.tar.gz
    cd cmake-3.12.3
    ./bootstrap
    gmake
    gmake install

    cd /tmp/
    curl -O https://ampl.com/demo/ampl.linux$1.tgz
    tar xzvf ampl.linux$1.tgz
    mv ampl.linux$1 /opt/

    rm -rf /tmp/*
fi

