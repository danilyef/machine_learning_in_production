1. Start Minikube

```bash
minikube start
```

2. Add Airflow Helm Stable Repo

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

3. Build custom docker image (with dependencies)

```bash
docker build -t yf19001/custom_airflow .
docker push yf19001/custom_airflow:latest
```

4. Install Airflow using Helm

```bash

export NAMESPACE=airflow
kubectl create namespace $NAMESPACE

helm install airflow apache-airflow/airflow --namespace $NAMESPACE --timeout 50m0s \
    --set images.airflow.repository=yf19001/custom_airflow \
    --set images.airflow.tag=latest \
    --set executor=KubernetesExecutor
```

5. Create volumes for pipelines:

```bash
kubectl apply -f volumes.yaml -n airflow
```

6. Port forward

```bash
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace $NAMESPACE
```

7. Start Dag in UI

