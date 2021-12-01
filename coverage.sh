#!/bin/bash
cd "`dirname "$0"`"
set -ex
# python -m pip install coverage
coverage run -m amplpy.tests
coverage report
coverage html
