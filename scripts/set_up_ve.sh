#!/bin/bash
# check <https://pypi.org> for existing packages

echo 'Setting up virtual enviroment for Linux'
python3 -m venv aml-venv

source aml-env/bin/activate
# just for testing

pip list