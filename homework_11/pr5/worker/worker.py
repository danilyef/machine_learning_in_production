from kafka import KafkaConsumer, KafkaProducer
from transformers import pipeline
import json
import os


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-1:9092")
REQUEST_TOPIC = "requests"
PREDICTION_TOPIC = "predictions"

sentiment_pipeline = pipeline("sentiment-analysis")

consumer = KafkaConsumer(
    REQUEST_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="sentiment_worker",
    auto_offset_reset="earliest"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


for message in consumer:
    request = message.value
    result = sentiment_pipeline(request["text"])[0]
    response = {"id": request["id"],"result":result}

    producer.send(PREDICTION_TOPIC,response)
