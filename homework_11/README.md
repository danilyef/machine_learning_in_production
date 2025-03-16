# Homework 11: Serving advanced

## Tasks:

- PR1: Write code for dynamic request batching for your model (you might use Triton, Seldon, or KServe for this).
- PR2: Write code for an ensemble of several models (you might use Triton, Seldon, or KServe for this).
- PR3: Write code for gRPC inference for your model server (you might use Triton, Seldon, or KServe for this).
- PR4: Write code for benchmarking your model server: report latency, RPS, etc.
- PR5: Write code for async inference for your models with the help of queue (Kafka, or any other queue).


### PR1: Dynamic request batching for your model

**Step 1: Build docker image**
```bash
docker build -t triton_transformer_server .
```

**Step 2: Run docker container**
```bash
docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models
```

**Step 3: Test**
```bash
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1,1],"data":["I am going"]}]}'
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[2,1],"data":["I am going","I am good"]}]}'

python client.py
```


### PR2: Ensemble of several models Triton

**Step 1: Build docker image**
```bash
docker build -t triton_transformer_server .
```

**Step 2: Run docker container**
```bash
docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models
```

**Step 3: Test**
```bash
python client.py
```



### PR3: gRPC inference for your model server Triton

**Step 1: Build docker image**
```bash
docker build -t triton_transformer_server .
```

**Step 2: Run docker container**
docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models

**Step 3: Test**
```bash     
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1,1],"data":["I am going"]}]}'
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[2,1],"data":["I am going","I am good"]}]}'

python client.py
```


### PR4: Benchmarking model server

**Step 1: Build docker image**
```bash 
docker build -t triton_transformer_server .
```

**Step 2: Run docker container**
docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models

**Step 3: Run locust**
```bash
locust -f locust_http.py --headless -u 10 -r 2 --run-time 1m  --host=http://localhost:8000
```

#### Explanation of locust command  

--headless → Runs without UI.
-u 10 → Simulates 10 concurrent users.
-r 2 → Spawns 2 users per second.
--run-time 1m → Runs for 1 minute.



### PR5: Async Kafka Inference: 

**Step 1: Build docker images**
```bash 
docker-compose up --build
```





