# Homework 10: Inference servers

## Tasks:

- PR1: Write code for Seldon API deployment of your model.
- PR2: Write code for KServe API integration with your model.
- PR3: Write code for Triton Inference Server deployment.
- PR4: Write code for Ray deployment.
- PR5: Write code for LLM deployment using TGI, vLLM, and LoRAX.


### PR3: Triton Inference Server deployment

**Step 1: Create a Model Repository**
```bash
mkdir -p model_repository
cp -r distilbert_ss/ model_repository/
```

**Step 2: build image container**
```bash
docker build -t triton_transformer_server .
```

**Step 3: run docker image**
```bash
docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models
```

**Step 4: Query the Server**
```bash
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1],"data":["I am going"]}]}'
```


### PR4: Ray deployment

**Step 1: Run Ray server**
```bash
serve run main:sentiment_analysis_app
```

**Step 2: Query the server**
```bash
python client.py
```


### PR5: vLLM and TGI

#### TGI

**Step 1: Create script and privileges:**

```bash
chmod +x run.sh
```

**Step 2: Start script:**

```bash
./tgi_inference.sh
```

**Step 3: Test script:**

```bash
curl 127.0.0.1:8080/generate_stream \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```


#### vLLM

**Step 1: build Dockerfile**
```bash
docker build -t zephyr-vllm .
```

**Step 2: Run dockerfile**
```bash
docker run --gpus all -p 8000:8000 zephyr-vllm
```

**Step 3:   Test**

```bash
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'
```