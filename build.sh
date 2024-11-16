#!/bin/bash

cwd=$(pwd)
echo "current directory ->" $cwd
echo "building..."
services_path=$cwd/services

echo $DOCKER_TOKEN | docker login --username $DOCKER_USER --password-stdin
docker buildx create --use

for service_path in $services_path/*; do
    service_name=$(basename $service_path)
    echo "building" $service_name
    pushd $service_path
    docker buildx build --push --platform linux/arm64/v8 \
        --tag $DOCKER_USER/overlord-$service_name:latest --file $service_path/Dockerfile .

    popd
done
