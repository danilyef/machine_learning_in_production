from dagster import  materialize, Definitions
from resources.resources import BaseModel, RawDatasetConfig
from assets.datasets import load_test_dataset,load_inference_results_wandb
from assets.models import load_model_wandb, inference_model

# Define the Dagster assets job
defs = Definitions(
    assets=[load_test_dataset, load_model_wandb, inference_model,load_inference_results_wandb],
    resources={
        "config_model": BaseModel(model_name="distilbert/distilbert-base-uncased-finetuned-sst-2-english",batch_size=16,num_epochs=3,learning_rate=2e-5),
        "config": RawDatasetConfig()
    }
)

if __name__ == "__main__":
    # Run the asset-based inference pipeline
    materialize(defs)
