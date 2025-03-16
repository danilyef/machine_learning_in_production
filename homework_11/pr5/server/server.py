from fastapi import FastAPI
from kafka import KafkaProducer, KafkaConsumer
import json
import uuid
import os

app = FastAPI()


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-2:9093")
REQUEST_TOPIC = "requests"
PREDICTION_TOPIC = "predictions"


consumer = KafkaConsumer(
    PREDICTION_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="result_consumer",
    auto_offset_reset="earliest"
)


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


@app.post("/predict")
async def send_request(text: str):
    request_id = str(uuid.uuid4())  
    message = {"id": request_id, "text": text}
    producer.send(REQUEST_TOPIC, message)
    return {"message": "Request sent", "request_id": request_id}


@app.get("/result/{request_id}")
async def get_result(request_id: str):
    messages = consumer.poll(timeout_ms=2000)
    if messages:
        for _, records in messages.items():
            for record in records:
                if record.value["id"] == request_id:
                    return record.value["result"]
    
    return {"error": "Result not found"}