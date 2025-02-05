Guide taken and tested from: https://docs.vllm.ai/en/v0.6.4/serving/deploying_with_k8s.html


1. Create a PVC , Secret and Deployment for vLLM

kubectl -f pvc.yaml

2. Create Deployment and service:

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

3. Test

curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'