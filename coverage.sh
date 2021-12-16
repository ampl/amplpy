#!/bin/bash
cd "`dirname "$0"`"
set -ex
# python -m pip install coverage
coverage run examples/test_examples.py
coverage run -a -m amplpy.tests
coverage run -a -m amplpy.tests_pep8
coverage report
coverage html
