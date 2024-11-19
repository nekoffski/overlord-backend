#!/bin/bash

cwd=$(pwd)
echo "current directory ->" $cwd
echo "building..."
services_path=$cwd/services
push=false

echo $DOCKER_TOKEN | docker login --username $DOCKER_USER --password-stdin

for service_path in $services_path/*; do
    service_name=$(basename $service_path)
    echo "building" $service_name
    pushd $service_path

    docker image build -t overlord-$service_name:latest --file $service_path/Dockerfile .
    docker tag overlord-$service_name $DOCKER_USER/overlord-$service_name

    if [ "$my_bool" = true ]; then
        docker push $DOCKER_USER/overlord-$service_name
    fi
    
    popd
done
