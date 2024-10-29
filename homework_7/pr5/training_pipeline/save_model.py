import torch
import shutil
import wandb
from pathlib import Path
import os

def save_trained_model():
    # Use the mounted volume path directly
    model_path = Path("/tmp/model.pth")
    # Ensure the directory exists

    model_state_dict = torch.load(model_path)

    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = 'my_project_api_key'

    # Initialize wandb
    wandb.init(project="mnist_training", name="model_upload")

    # Save and upload the model to wandb
    artifact = wandb.Artifact('mnist_model', type='model')
    with artifact.new_file('model.pth', mode='wb') as f:
        torch.save(model_state_dict, f)
    wandb.log_artifact(artifact)

    wandb.finish()

    print("Model uploaded to Weights & Biases successfully")

if __name__ == "__main__":
    save_trained_model()