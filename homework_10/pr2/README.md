1. minikube start --cpus=10 --memory=24576


2. Install Kuberay:

helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.2

kubectl get pods


3. Apply rayservice file:

kubectl apply -f rayservice.yaml

4. Get port:

kubectl port-forward service/rayservice-sample-serve-svc 8000
