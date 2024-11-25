#!/bin/bash

sudo apt-get install -y python3.12-venv
python -m venv ./venv

source ./venv/bin/activate
python -m pip install build grpcio-tools

pushd lib

rm -f ./src/overlord/proto/*pb2*.py
python -m grpc_tools.protoc -Iproto --python_out=./src/overlord/proto \
    --pyi_out=./src/overlord/proto --grpc_python_out=./src/overlord/proto ./proto/*.proto
sed -i 's/^import \(.\+\) as/from . import \1 as/' ./src/overlord/proto/*.py*
python -m build

protoc -Iproto --js_out=import_style=commonjs:dist \
    --grpc-web_out=import_style=commonjs,mode=grpcwebtext:dist ./proto/*.proto
