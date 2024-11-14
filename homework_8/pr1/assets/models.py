import os
import wandb
import datasets
import torch
from dagster import asset, AssetIn, Output, MetadataValue
from transformers import Trainer, TrainingArguments, DistilBertForSequenceClassification
from resources.resources import BaseModel
import pandas as pd


@asset(description="Training step",group_name="training_pipeline",ins={"train_dataset": AssetIn(), "val_dataset": AssetIn()})
def train_model(train_dataset: datasets.Dataset, val_dataset: datasets.Dataset, config_model: BaseModel):
    # Initialize model
    model = config_model.PretrainedModel()
    
    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=config_model.num_epochs,
        per_device_train_batch_size=config_model.batch_size,
        per_device_eval_batch_size=config_model.batch_size,
        learning_rate=config_model.learning_rate,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        no_cuda=True #for mac 
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    # Train the model
    trainer.train()
    
    # Save the best model
    best_model_path = "./best_model"
    trainer.save_model(best_model_path)
    
    return Output(
        model,
        metadata={
            "model_name": MetadataValue.text(config_model.model_name),
            "training_epochs": MetadataValue.int(training_args.num_train_epochs),
            "device": MetadataValue.text(str(device))
        },
    )


@asset(description="Save model to wandb",group_name="training_pipeline",ins={"train_model": AssetIn()})
def save_model_wandb(train_model):
    # Initialize wandb
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'
    wandb.init(project="sentiment-analysis", name="model-upload")
    
    # Create a wandb artifact
    artifact = wandb.Artifact(
        name="sentiment-model", 
        type="model",
        description="DistilBERT model trained for sentiment analysis"
    )
    
    # Add the model directory to the artifact
    artifact.add_dir("./best_model")
    
    # Log the artifact to wandb
    wandb.log_artifact(artifact)
    
    # Close wandb run
    wandb.finish()
    
    return Output(
        value="Model saved to wandb",
        metadata={
            "wandb_project": MetadataValue.text("sentiment-analysis"),
            "artifact_name": MetadataValue.text("sentiment-model")
        }
    )


@asset(description="Load model from wandb",group_name="inference_pipeline")
def load_model_wandb():
    # Initialize wandb
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'
    wandb.init(project="sentiment-analysis", name="model-download")
    
    # Get the latest version of the model artifact
    artifact = wandb.use_artifact('sentiment-analysis/sentiment-model:latest')
    
    # Download the artifact
    model_dir = artifact.download()
    
    # Load the model
    model = DistilBertForSequenceClassification.from_pretrained(model_dir)
    
    # Close wandb run
    wandb.finish()
    
    return Output(
        model,
        metadata={
            "wandb_project": MetadataValue.text("sentiment-analysis"),
            "artifact_name": MetadataValue.text("sentiment-model"),
            "model_dir": MetadataValue.text(model_dir)
        }
    )

@asset(description="Inference step",group_name="inference_pipeline",ins={"load_model_wandb": AssetIn(), "load_test_dataset": AssetIn()})
def inference_model(load_model_wandb: DistilBertForSequenceClassification, load_test_dataset: datasets.Dataset):
    # Set model to evaluation mode
    model = load_model_wandb.eval()
    
    # Initialize lists to store predictions
    predictions = []
    
    # Run inference
    for batch in load_test_dataset:
        # Get model predictions
        with torch.no_grad():
            outputs = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
            logits = outputs.logits
            predicted_label = torch.argmax(logits, dim=1).item()
            
        predictions.append(predicted_label)
    
    # Create a pandas DataFrame with predictions
    df_predictions = pd.DataFrame({
        'Predicted_Label': predictions
    })
    
    return Output(
        value=df_predictions,
        metadata={
            "num_samples": MetadataValue.int(len(predictions))
        }
    )


