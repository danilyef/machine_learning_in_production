from dagster import  materialize, Definitions
from resources.resources import BaseModel, RawDatasetConfig
from assets.datasets import raw_datasets, tokenizer, processed_datasets, train_dataset, val_dataset, test_dataset, save_test_dataset
from assets.models import train_model, save_model_wandb

# Define the Dagster assets job
defs = Definitions(
    assets=[raw_datasets, tokenizer, processed_datasets, train_dataset, val_dataset, test_dataset, save_test_dataset, train_model,save_model_wandb],
    resources={
        "config_model": BaseModel(model_name="distilbert/distilbert-base-uncased-finetuned-sst-2-english",batch_size=16,num_epochs=3,learning_rate=2e-5),
        "config": RawDatasetConfig()
    }
)

if __name__ == "__main__":
    # Run the asset-based inference pipeline
    materialize(defs)
