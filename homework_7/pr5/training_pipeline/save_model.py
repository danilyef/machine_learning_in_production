import torch
import shutil
import wandb
from pathlib import Path
import os

def save_trained_model():
    # Use the mounted volume path directly
    #model_path = Path("/opt/airflow/data/model/model.pth")
    model_path = Path("/tmp/model.pth")
    # Ensure the directory exists
    #model_path.parent.mkdir(exist_ok=True, parents=True)

    # Check if the model file exists
    #if not model_path.exists():
        #raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load the trained model
    #torch.save(model_obj.state_dict(), artifact_path / "model.pth")
    model_state_dict = torch.load(model_path)

    #print(model_state_dict['1.weight'][:2,:5])

    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'

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