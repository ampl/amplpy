#!/bin/bash

if [ "$#" -eq 0 ]; then
  	echo "Usage: $0 [32|64]"
else
    cd /tmp/
    wget http://www.cmake.org/files/v3.0/cmake-3.0.0.tar.gz --no-check-certificate
    tar xzvf cmake-3.0.0.tar.gz
    cd cmake-3.0.0
    ./bootstrap
    gmake
    gmake install

    cd /tmp/
    wget http://ampl.com/demo/ampl.linux$1.tgz
    tar xzvf ampl.linux$1.tgz
    mv ampl.linux$1 /opt/

    rm -rf /tmp/*
fi

