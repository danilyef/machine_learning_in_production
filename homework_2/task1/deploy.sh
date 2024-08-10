#!/bin/bash

# Variables
IMAGE_NAME="python-server"
TAG="latest"
DOCKER_USER="yf19001"
REPO_NAME="${DOCKER_USER}/${IMAGE_NAME}:${TAG}"

# Build image
echo "Building Docker image..."
docker build -t ${REPO_NAME} .


if [$? -ne 0]; then
    echo "Docker build failed. Exiting."
    exit 1
fi 


# Login into docker hub
echo "Logging in to Docker Hub..."
docker login -u yf19001


if [$? -ne 0]; then
    echo "Docker login failed. Exiting"
    exit 1
fi

# Push docker image
docker push ${REPO_NAME}


if [ $? -ne 0 ]; then
    echo "Docker push failed. Exiting."
    exit 1
fi

echo "Docker image pushed successfully to Docker Hub."