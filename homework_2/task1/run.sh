#!/bin/bash

# Variables
CONTAINER_NAME="app-ml-test-run"
IMAGE_NAME="python-run"
TAG="latest"


# Build Image
echo "Building Docker image..."
docker build -t "${IMAGE_NAME}:${TAG}" -f Dockerfile.run .

if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi 

# Run and exit Image
echo "Run Docker image..."
docker run -it --rm --name "${CONTAINER_NAME}" "${IMAGE_NAME}:${TAG}"

if [ $? -ne 0 ]; then
    echo "Docker Run failed. Exiting."
    exit 1
fi 

echo "Docker image exited"



