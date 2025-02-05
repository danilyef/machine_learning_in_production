# Homework 10: Inference servers

## Tasks:

- PR1: Write code for Triton Inference Server deployment.
- PR2: Write code for Ray deployment.
- PR3: Write code for LLM deployment using TGI, vLLM, and LoRAX.


### PR1: Triton Inference Server deployment

**Step 1: Create a Model Repository**
```bash
mkdir -p model_repository
cp -r distilbert_ss/ model_repository/
```

**Step 2: Download Model and save in model_repository folder**


**Step 3: Save yaml file for deployment and service in current folder**

**Step 4: Make a mount, such that minikbue has access to the folder**
```bash
minikube mount $PWD:/mnt/data
```

**Step 5: This command fetches the necessary environment variables to configure your shell to use the Docker daemon inside the Minikube VM.**

```bash
eval $(minikube -p minikube docker-env)
```

**Step 6: Build image container**
```bash
docker build -t custom_triton .
```

**Step 7: Apply deployment and service**
```bash
 kubectl apply -f deployment_service.yaml
```

**Step 8: Expose ports**
```bash
kubectl get svc triton-inference-service
```

**Step 9: Internal ip of the node**

```bash
kubectl get nodes -o wide
```

**Step 10: check existence of the model**

```bash
curl http://192.168.49.2:<port>/v2/models/<model_name>
```

**Step 11: test request**

```bash
curl -X POST 192.168.49.2:<port>/v2/models/<model_name>/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1],"data":["I am going"]}]}'
```


### PR2: Ray deployment

**Step 1: Start minikube**
```bash
minikube start --cpus=10 --memory=24576
```

**Step 2: Install Kuberay**
```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.2

kubectl get pods
```

**Step 3: Apply rayservice file**
```bash
kubectl apply -f rayservice.yaml
```

**Step 4: Get port**
```bash
kubectl port-forward service/rayservice-sample-serve-svc 8000
```


**Step 5: Test request**
```bash
curl -X POST -H "Content-Type: application/json" localhost:8000/text_sentiment -d '{"text": "I am going to the store"}'
```

### PR3: vLLM and TGI

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


#### vLLM on Kubernetes
Guide taken and tested from: https://docs.vllm.ai/en/v0.6.4/serving/deploying_with_k8s.html

**Step 1: Create a PVC , Secret and Deployment for vLLM**
```bash
kubectl -f pvc.yaml
```

**Step 2: Create Deployment and service**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

**Step 3: Test**
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

