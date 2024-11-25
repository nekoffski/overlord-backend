#!/bin/bash
CONFIG_DIR=$(pwd)/config docker compose --file ./compose.yaml up --remove-orphans