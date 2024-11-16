#!/bin/bash

ip=$1
user=$2
creds=$user@$ip
cwd=$(pwd)
deploy_scripts=$cwd/deploy-scripts

echo "cwd ->" $cwd
ping $ip -c 1

execute_remotely() {
    cat $1 | ssh $creds
}

scp -r $deploy_scripts/config $creds:~

execute_remotely $deploy_scripts/setup-nginx.sh
execute_remotely $deploy_scripts/pull-containers.sh
