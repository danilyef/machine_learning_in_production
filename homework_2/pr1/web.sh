#!/bin/bash

# Variables
IMAGE_NAME="python-server"
TAG="latest"
DOCKER_USER="yf19001"
REPO_NAME="${DOCKER_USER}/${IMAGE_NAME}:${TAG}"
CONTAINER_NAME="web-server"

# Build image
echo "Building Docker image..."
docker build -t ${REPO_NAME} -f Dockerfile.web .


if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi 


# Login into docker hub
echo "Logging in to Docker Hub..."
docker login -u yf19001


if [ $? -ne 0 ]; then
    echo "Docker login failed. Exiting"
    exit 1
fi

# Run Web Server:
docker run -it --rm -p 80:80 --name "${CONTAINER_NAME}" "${REPO_NAME}"
curl http://127.0.0.1:80

# Push docker image
docker push ${REPO_NAME}


if [ $? -ne 0 ]; then
    echo "Docker push failed. Exiting."
    exit 1
fi

echo "Docker image pushed successfully to Docker Hub."