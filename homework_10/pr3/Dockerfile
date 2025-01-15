FROM nvcr.io/nvidia/tritonserver:23.10-py3

# Copy requirements.txt into the container
COPY requirements.txt /workspace/

# Install dependencies from requirements.txt
RUN pip install -r /workspace/requirements.txt
