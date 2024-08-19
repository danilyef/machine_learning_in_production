# Homework 2

This repository contains tasks related to Docker, Kubernetes, and GitHub Actions.

## Structure

The repository is organized into the following directories:

- `homework_2/task1/`: Contains Docker-related tasks.
- `homework_2/task2/`: Contains Kubernetes-related tasks.
- `.github/workflows/`: Contains the GitHub Actions workflows.

### Task 1: Docker

#### PR1: `homework_2/task1`

This task involves working with Docker. The following scripts are available:

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

#### PR2: `.github/workflows`

This directory contains GitHub Actions workflows used for CI/CD automation.

### Task 3: Kubernetes

#### PR3: `homework_2/task2`

This task involves working with Kubernetes resources.

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
