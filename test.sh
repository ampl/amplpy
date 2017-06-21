#!/bin/bash
BASEDIR=`dirname $0`
BASEPATH=`realpath $BASEDIR`
cd $BASEPATH

source venv/bin/activate
pip install -r requirements.txt
nosetests tests --with-coverage --cover-erase --cover-html --cover-html-dir=$BASEPATH/cover
