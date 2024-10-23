### Deploying Kubeflow pipelines

#### Local Deployment:

1. Install kubernetes(minikube) 

    - if you are using minikube, you need to install Docker desktop before installing minikube.

2. Start minikube:

    ```
    minikube start
    ```

3. Define version of kubeflow pipelines:

    ```
    export PIPELINE_VERSION=2.3.0
    ```

4. Configures all resource on the kubernetes clustersm which are needed to run Kubeflow pipelines:

    ```
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
    ```

5. Check the status of a Custom Resource Definition (CRD) in a Kubernetes cluster. Its needed because Kubeflow pipeline heavily relies on cusom resources.

    ```
    kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
    ```

6. Deploying Kubeflow Pipelines resources to the development environment on kubernetes.

    ```
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
    ```
7. Create pipeline (yaml file) and upload it by using kufeflow ui.






