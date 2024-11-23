#!/bin/bash

cwd=$(pwd)
echo "current directory ->" $cwd
echo "building..."
services_path=$cwd/services
push=false

# build python lib
lib/build.sh
lib_dist=$cwd/lib/dist

echo $DOCKER_TOKEN | docker login --username $DOCKER_USER --password-stdin

build_container () {
    service_path=$1
    service_name=$(basename $service_path)
    echo "building" $service_name
    cp -r $lib_dist $service_path

    pushd $service_path
    docker image build -t overlord-$service_name:latest \
            --file $service_path/Dockerfile .
    docker tag overlord-$service_name $DOCKER_USER/overlord-$service_name
    rm -rf $service_path/dist

    if [ "$push" = true ]; then
        docker push $DOCKER_USER/overlord-$service_name
    fi

    popd
}

if [ "$1" = "all" ]; then 
    for service_path in $services_path/*; do
        build_container $service_path
    done
else
    build_container $services_path/$1
fi
