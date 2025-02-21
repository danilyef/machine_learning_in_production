
docker build -t triton_transformer_server .

docker run --gpus all --rm --shm-size=1G -p 8000:8000 -p 8001:8001 -p 8002:8002 -v $(pwd)/model_repository:/models triton_transformer_server tritonserver --model-repository=/models

curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1,1],"data":["I am going"]}]}'
curl -X POST localhost:8000/v2/models/distilbert_sst2/infer -d '{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[2,1],"data":["I am going","I am good"]}]}'

python client.py
