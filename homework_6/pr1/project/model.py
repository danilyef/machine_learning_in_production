from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch


class TextClassifier:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_name)
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        predicted_class_id = torch.argmax(outputs.logits, dim=1).item()
        return self.model.config.id2label[predicted_class_id]

    def predict_proba(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        return probabilities.squeeze().max().item()
