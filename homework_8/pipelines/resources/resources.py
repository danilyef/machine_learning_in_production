from dagster import asset, Config, Output
from dagster import ConfigurableResource, MetadataValue
import datasets
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import numpy as np
import torch


class RawDatasetConfig(Config):
    dataset_name: str = "stanfordnlp/sst2"
    dataset_path: str = "some/path/to/dataset/sst2"
    seed: int = 42
    train_size: float = 0.8



class BaseModel(ConfigurableResource):
    model_name: str
    batch_size: int = 16
    num_epochs: int = 1
    learning_rate: float = 2e-5
    
    def PretrainedTokenizer(self):
        return DistilBertTokenizer.from_pretrained(self.model_name)
    
    def PretrainedModel(self):
        return DistilBertForSequenceClassification.from_pretrained(self.model_name)