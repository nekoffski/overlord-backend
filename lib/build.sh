#!/bin/bash

sudo apt-get install -y python3-build python3.12-venv
pushd lib
python -m build
