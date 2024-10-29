import wandb
from pathlib import Path
import os

def load_model():
    # Use the mounted volume path directly
    
    model_path = Path("/tmp/")
    
    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = 'my_project_api_key'

    # Initialize wandb with existing project
    wandb.init(project="mnist_training", name="model_download", resume=True)

    # Save and upload the model to wandb
    artifact = wandb.use_artifact("mnist_model:latest", type="model")
    model_dir = artifact.download(root=model_path)
    wandb.finish()


if __name__ == "__main__":
    load_model()