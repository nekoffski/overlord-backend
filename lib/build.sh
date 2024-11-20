#!/bin/bash

sudo apt-get install -y python3.12-venv
python -m venv ./venv

source ./venv/bin/activate
python -m pip install build grpcio-tools

pushd lib

python -m grpc_tools.protoc -Iproto --python_out=./dist --pyi_out=./dist --grpc_python_out=./dist ./proto/*
cp ./dist/*{.py,.pyi} ./src/overlord/models

python -m build
