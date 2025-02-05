from starlette.requests import Request
from typing import Dict
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from ray import serve
import torch
from torch.nn.functional import softmax


@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probabilities = softmax(logits, dim=-1)

        predicted_class_id = logits.argmax(dim=-1).item()

        probability = probabilities[0,predicted_class_id]
        output_label = self.model.config.id2label[predicted_class_id]

        return {"label": output_label, "probability": probability.item()}


sentiment_analysis_app = SentimentAnalysisDeployment.bind()