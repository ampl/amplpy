#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
nosetests tests --with-coverage --cover-erase --cover-html
