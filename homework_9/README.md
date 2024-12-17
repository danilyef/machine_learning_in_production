# Homework 9: API serving

## Tasks:

- PR1: Write a Streamlit UI for serving your model, with tests and CI integration.
- PR2: Write a Gradio UI for serving your model, with tests and CI integration.
- PR3: Write a FastAPI server for your model, with tests and CI integration.
- PR4: Write a Kubernetes deployment YAML (Deployment, Service) for your model's API.
- PR5: Write a Kubernetes deployment YAML (Deployment, Service) for your model's UI (Streamlit, Gradio).


### PR1: Streamlit UI

- **How to run**:
```bash
streamlit run main.py
```

- **How to test**:
```bash
pytest tests/streamlit/test_model.py
```

### PR2: Gradio UI

- **How to run**:
```bash
python main.py
```

- **How to test**:
```bash
pytest tests/gradio/test_model.py
```

### PR3: FastAPI server

- **How to run**:
```bash
cd homework_9
uvicorn pr3.app:app --reload
```

- **How to test**:
```bash
pytest tests/fastapi/test_model.py
```

### PR4: Kubernetes deployment YAML (Deployment, Service) for your model's API


**correct home directory**:

```bash
cd homework_9/pr4
```

**start minikube**:

```bash
minikube start
eval $(minikube -p minikube docker-env)
```


**build docker image**:

```bash
docker build -t fastapi-app:latest .
```

**deploy to minikube**:

```bash
kubectl apply -f k8s_deployment.yaml
```

**get url**:

```bash
minikube service fastapi-service --url
```

**test predict**:

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"text": "this is good"}' \
    http://127.0.0.1:51561/predict
```

### PR5: Kubernetes deployment YAML (Deployment, Service) for your model's UI (Streamlit, Gradio)

**correct home directory**:

```bash
cd homework_9/pr5
```

**start minikube**:

```bash
minikube start
eval $(minikube -p minikube docker-env)
```


**build docker image**:

```bash
docker build -t streamlit-app:latest .
```

**deploy to minikube**:

```bash
kubectl apply -f k8s_deployment.yaml
```

**get url**:

```bash
minikube service streamlit-service --url
```


**test predict**:

```bash
new url: http://192.168.99.100:30000/ (or other)
```



### Useful Information

In Kubernetes, **`type: NodePort`** is used in a Service when you want to access your application from outside the Kubernetes cluster (like your laptop or local browser).

Here’s why you might use it in simple terms:

---

**1. Kubernetes Runs on Its Own Network**
- Kubernetes creates an internal network for all the Pods.
- By default, this network isn’t accessible from the outside (e.g., your computer).

---

**2. Services Expose Pods**
- A **Service** connects your app (running in Pods) to the outside world.
- **`type: NodePort`** exposes your app on a specific port on every node in your cluster.

---

**3. Why Use `NodePort`?**
- When you set `type: NodePort`, Kubernetes assigns a port (like `30000-32767`) on the node's IP address.
- You can now access your app by visiting:
  ```
  http://<node-ip>:<node-port>
  ```
  For example:
  ```
  http://192.168.99.100:30000
  ```
  Here, `192.168.99.100` is the Minikube node's IP, and `30000` is the NodePort.

---

**4. Why Not Use ClusterIP?**
- By default, Services use **`type: ClusterIP`**, which only allows access *within* the Kubernetes cluster.
- This is useful for internal communication between apps but not for external access.

---

**5. Why NodePort is Good for Minikube**
- In Minikube, you're running Kubernetes on your local machine.
- Using `NodePort` is a quick and simple way to test and access your app from your browser or other devices on the same network.

---

**In Summary**
- **`type: NodePort`** makes your app accessible outside Kubernetes on a specific port.
- This is great for testing or development, especially in Minikube. 
- Later, in production, you might use other Service types (like `LoadBalancer` or `Ingress`) for more advanced routing.