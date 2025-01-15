# Homework 10: Inference servers

## Tasks:

- PR1: Write code for Seldon API deployment of your model.
- PR2: Write code for KServe API integration with your model.
- PR3: Write code for Triton Inference Server deployment.
- PR4: Write code for Ray deployment.
- PR5: Write code for LLM deployment using TGI, vLLM, and LoRAX.
- PR6: Write code for LLM deployment with ModalLab.


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