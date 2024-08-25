# MinIO Deployment 


## 1. Local Deployment

### Prerequisites
- MinIO binary downloaded from the official website

### Steps
1. Download MinIO from the website
2. Make programm executable:
3. Run MinIO:
   ```
   ./minio server /data
   ```
4. Access the MinIO browser at `http://127.0.0.1:port`

## 2. Docker Deployment


### Steps
1. Pull the MinIO Docker image:
2. Run MinIO container:
3. Access the MinIO browser at `http://127.0.0.1:port`

## 3. Kubernetes (K8S) Deployment



### Steps
1. Create a MinIO deployment YAML file (minio-deployment.yaml):
   
2. Apply the deployment:
   ```
   kubectl apply -f deployment.yaml
   ```

3. Expose the MinIO service:
   ```
   kubectl expose deployment minio --type=LoadBalancer --port=9000
   ```

4. Get the external IP:
   ```
   kubectl get services minio
   ```
5. Access MinIO using the external IP and port 9000

