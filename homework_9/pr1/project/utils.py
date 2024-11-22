from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Model:
    def __init__(self,tokenizer_name,model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
        label_id = prediction.argmax().item()
        return "POSITIVE" if label_id == 1 else "NEGATIVE"
        
    def predict_proba(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return probabilities[0].tolist()  # Return probabilities for all classes