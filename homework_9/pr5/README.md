## correct home directory

```bash
cd homework_9/pr5
```

## start minikube

```bash
minikube start
eval $(minikube -p minikube docker-env)
```


## build docker image

```bash
docker build -t streamlit-app:latest .
```

## deploy to minikube

```bash
kubectl apply -f k8s_deployment.yaml
```

## get url

```bash
minikube service streamlit-service --url
```


## test predict

```bash
new url: http://192.168.99.100:30000/ (or other)
```




In Kubernetes, **`type: NodePort`** is used in a Service when you want to access your application from outside the Kubernetes cluster (like your laptop or local browser).

Here’s why you might use it in simple terms:

---

### **1. Kubernetes Runs on Its Own Network**
- Kubernetes creates an internal network for all the Pods.
- By default, this network isn’t accessible from the outside (e.g., your computer).

---

### **2. Services Expose Pods**
- A **Service** connects your app (running in Pods) to the outside world.
- **`type: NodePort`** exposes your app on a specific port on every node in your cluster.

---

### **3. Why Use `NodePort`?**
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

### **4. Why Not Use ClusterIP?**
- By default, Services use **`type: ClusterIP`**, which only allows access *within* the Kubernetes cluster.
- This is useful for internal communication between apps but not for external access.

---

### **5. Why NodePort is Good for Minikube**
- In Minikube, you're running Kubernetes on your local machine.
- Using `NodePort` is a quick and simple way to test and access your app from your browser or other devices on the same network.

---

### **In Summary**
- **`type: NodePort`** makes your app accessible outside Kubernetes on a specific port.
- This is great for testing or development, especially in Minikube. 
- Later, in production, you might use other Service types (like `LoadBalancer` or `Ingress`) for more advanced routing.