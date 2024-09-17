import wandb
import os
from transformers import DistilBertForSequenceClassification

def main():
    os.environ["WANDB_API_KEY"] = "0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384"
    
    # Initialize W&B
    wandb.init(project="model_saving", name="distilbert_run")

    # Load or create your DistilBert model
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    # Log the model to W&B
    wandb.watch(model)

    # After training, save the model
    model_artifact = wandb.Artifact("distilbert_model", type="model")
    model.save_pretrained("./distilbert_model")
    model_artifact.add_dir("./distilbert_model")
    wandb.log_artifact(model_artifact)

    # End the W&B run
    wandb.finish()

if __name__ == "__main__":
    main()