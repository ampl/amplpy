#!/bin/bash
cd "`dirname "$0"`"
cd ..

if [ "$#" -ne 1 ]; then
  	echo "Usage: $0 <URL>"
    exit 1
fi
set -ex

URL=$1
PACKAGE=`basename $URL`
curl -k -L -O $URL
if [[ $PACKAGE == *.zip ]]; then
    unzip $PACKAGE
else
    tar xzvf $PACKAGE
fi
rm $PACKAGE
mv ampl.* ampl
cd ampl
pwd
