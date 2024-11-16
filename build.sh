#!/bin/bash

cwd=$(pwd)
echo "current directory ->" $cwd
echo "building..."
services_path=$cwd/services

for service_path in $services_path/*; do
    service_name=$(basename $service_path)
    echo "building" $service_name
    pushd $service_path
    docker image build -t overlord-$service_name:latest --file $service_path/Dockerfile .
    echo $DOCKER_TOKEN | docker login --username $DOCKER_USER --password-stdin
    docker tag overlord-$service_name $DOCKER_USER/overlord-$service_name
    docker push $DOCKER_USER/overlord-$service_name
    popd
done
