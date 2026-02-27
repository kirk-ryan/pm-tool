#!/bin/bash

# Stop and remove the Docker container
docker stop pm-container
docker rm pm-container

echo "App stopped"
