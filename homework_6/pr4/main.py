import wandb
import os
from transformers import DistilBertForSequenceClassification

def main():
    #os.environ["WANDB_API_KEY"] = "define_your_key"
    
    wandb.init(project="model_saving", name="distilbert_run")

    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    wandb.watch(model)

    model_artifact = wandb.Artifact("distilbert_model", type="model")
    model.save_pretrained("./distilbert_model")
    model_artifact.add_dir("./distilbert_model")
    wandb.log_artifact(model_artifact)

    wandb.finish()

if __name__ == "__main__":
    main()