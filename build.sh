#!/bin/bash

cwd=$(pwd)
echo "current directory ->" $cwd

function build {
    echo "building..."
    services_path=$cwd/services

    for service_path in $services_path/*; do
        service_name=$(basename $service_path)
        echo "building" $service_name
        pushd $service_path
        docker image build -t overlord-$service_name:latest --file $service_path/Dockerfile .
        popd
    done
}

function deploy {
    echo "deploying..."
}

if [ "$1" = '--build' ]; then
    build
elif [ "$1" = '--deploy' ]; then
    deploy
else
    echo "ERROR: specify either --build or --deploy"
    exit -1
fi
