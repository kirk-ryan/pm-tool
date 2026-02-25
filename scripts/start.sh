#!/bin/bash

# Build and run the Docker container
docker rm -f pm-container 2>/dev/null || true
docker build -t pm-app .
docker run -d --name pm-container -p 8000:8000 pm-app

echo "App started at http://localhost:8000"