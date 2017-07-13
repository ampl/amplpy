#!/bin/bash
BASEDIR=`dirname $0`
BASEPATH=`realpath $BASEDIR`
cd $BASEPATH

source venv/bin/activate
pip install -r requirements.txt
pip install . --upgrade
nosetests amplpy.tests examples --with-coverage --cover-erase --cover-html --cover-html-dir=$BASEPATH/cover --cover-package amplpy
