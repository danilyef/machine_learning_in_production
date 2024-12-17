# Homework 2: Infrastructure setup

This repository contains tasks related to Docker, Kubernetes, and GitHub Actions.


## Tasks:

- PR1: Write a dummy Dockerfile with a simple server and push it to your docker hub or github docker registry.
- PR2: Write CI/CD pipeline with github action that does this for each PR.
- PR3: Write YAML definition for Pod, Deployment, Service, and Job with your Docker image, Use minikube/kind for testing it.Install k9s tool.

### Task 1: Docker

- folder: `homework_2/pr1`
- This task involves working with Docker. The following scripts are available:

1. **First Docker Container:**
   - **Purpose**: Builds and runs a task that prints output.
   - **How to Run**: Use the `run.sh` script.
   - **Command**: 
     ```bash
     ./run.sh
     ```

2. **Second Docker Container:**
   - **Purpose**: Starts a web server.
   - **How to Run**: Use the `web.sh` script.
   - **Command**: 
     ```bash
     ./web.sh
     ```


### Task 2: GitHub Actions

- folder: `.github/workflows`
- This directory contains GitHub Actions workflows used for CI/CD automation.

### Task 3: Kubernetes

- folder: `homework_2/pr3`
- This task involves working with Kubernetes resources.

1. **Pod**:
   - **Command**: 
     ```bash
     kubectl create -f homework_2/task2/pod.yaml
     ```

2. **Job**:
   - **Command**: 
     ```bash
     kubectl create -f homework_2/task2/job.yaml
     ```

3. **Deployment and Server**:
   - **Command**: 
     ```bash
     kubectl create -f homework_2/task2/deployment_service.yaml
     ```
