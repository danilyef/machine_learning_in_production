# Base image with Python and CUDA
FROM nvidia/cuda:12.1.1-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip git wget curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Expose the port for the API server
EXPOSE 8000

# Start the vLLM API server
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "Qwen/Qwen2.5-1.5B-Instruct"]