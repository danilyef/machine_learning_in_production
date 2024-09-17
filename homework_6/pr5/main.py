

import lit_nlp
from lit_nlp.api import dataset as lit_dataset
from lit_nlp.api import types
from lit_nlp.api import model 
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import pathlib
import os

from absl import flags



class TextClassifier:
    def __init__(self, model_name="./model"):
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



class MultiNLIData(lit_dataset.Dataset):
	"""Loader for MultiNLI development set."""

	NLI_LABELS = ['POSITIVE', 'NEGATIVE']

	def __init__(self, path: str):
		df = pd.read_parquet(path)
		self._examples = [{
			'text': row['text'],
			'label': row['label'],
		} for _, row in df.iterrows()]

	def spec(self) -> types.Spec:
		return {
			'text': types.TextSegment(),
			'label': types.CategoryLabel(vocab=self.NLI_LABELS),
		}

class NLIModel(model.Model):

	NLI_LABELS = ['POSITIVE', 'NEGATIVE']

	def __init__(self):
		self.model = TextClassifier()

	# LIT API implementations
	def predict(self, inputs):
		"""Predict on a stream of examples."""
		predictions = []
		for input_data in inputs:
			text = input_data['text']
			label = self.model.predict(text)
			probability = self.model.predict_proba(text)
			predictions.append({
				'label': label,
				'probability': probability
			})
		return predictions

	def input_spec(self) -> types.Spec:
		"""Describe the inputs to the model."""
		return {
			'text': types.TextSegment(),
		}

	def output_spec(self) -> types.Spec:
		"""Describe the model outputs."""
		return {
			'label': types.CategoryLabel(vocab=self.NLI_LABELS),
			'probability': types.RegressionScore(min_val=0, max_val=1)
		}



def main():
	# MulitiNLIData implements the Dataset API
	datasets = {
		'mnli_matched': MultiNLIData('/Users/daniil.yefimov/Desktop/Github/machine_learning_in_production/homework_6/pr5/data/data.parquet'),
		'mnli_mismatched': MultiNLIData('/Users/daniil.yefimov/Desktop/Github/machine_learning_in_production/homework_6/pr5/data/data.parquet'),
	}

	# NLIModel implements the Model API
	models = {
		'model': NLIModel()
	}

	client_root = lit_nlp.dev_server.get_default_client_root()
	lit_demo = lit_nlp.dev_server.Server(models, datasets, port=4321, client_root=client_root)
	lit_demo.serve()

if __name__ == '__main__':
	main()