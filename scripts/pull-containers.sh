#!/bin/bash

sudo docker compose -f ./config/compose.yaml down

sudo docker pull nyek0/overlord-web:latest

sudo docker compose -f ./config/compose.yaml up -d
