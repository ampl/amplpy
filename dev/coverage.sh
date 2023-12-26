#!/bin/bash
cd "`dirname "$0"`"
cd ..
set -ex

# python -m pip install coverage
coverage run examples/test_examples.py
coverage run -a -m amplpy.tests_camel
coverage run -a -m amplpy.tests
coverage report
coverage html
