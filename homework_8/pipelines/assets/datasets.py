from dagster import asset, Output,AssetIn
from dagster import MetadataValue
import datasets
from resources.resources import RawDatasetConfig, BaseModel
import os
import wandb
import pandas as pd



@asset(description="Raw dataset",group_name="training_pipeline")
def raw_datasets(config: RawDatasetConfig):
    dataset = datasets.load_dataset(config.dataset_name)

    '''
    format_data = pd.DataFrame(dataset_path)
    train, test= train_test_split(format_data,
                                   random_state=config.seed,
                                   train_size=config.train_size)

    validation, inference = train_test_split(test,
                                random_state=config.seed,
                                train_size=.8)
    dataset_train = datasets.Dataset.from_pandas(train)
    dataset_validation = datasets.Dataset.from_pandas(validation)
    dataset_inference = datasets.Dataset.from_pandas(inference)

    dataset = datasets.DatasetDict({"train": dataset_train, "validation": dataset_validation, "inference": dataset_inference})

    '''


    return Output(dataset, metadata= {"Train dataset size": len(dataset['train']), "Validation dataset size": len(dataset['validation']), "Test dataset size": len(dataset['test'])})



@asset(description= "HuggingFace Tokenizer",group_name="training_pipeline")
def tokenizer(config_model: BaseModel):
    bert_tokenizer = config_model.PretrainedTokenizer()
    return Output(
        bert_tokenizer,
        metadata={"model_name": MetadataValue.text(config_model.model_name)},
    )


@asset(description="Processed dataset",group_name="training_pipeline",ins={"raw_datasets": AssetIn(),"tokenizer": AssetIn()})
def processed_datasets(raw_datasets, tokenizer):
    tokenized_dataset = datasets.DatasetDict()
    tokenized_dataset["train"] = raw_datasets["train"].map(
        lambda x: tokenizer(x["sentence"], truncation=True, padding="max_length", max_length=512), batched=True, remove_columns=["sentence", "idx"]
    )
    tokenized_dataset["validation"] = raw_datasets["validation"].map(
        lambda x: tokenizer(x["sentence"], truncation=True, padding="max_length", max_length=512), batched=True, remove_columns=["sentence", "idx"]
    )
    tokenized_dataset["test"] = raw_datasets["test"].map(
        lambda x: tokenizer(x["sentence"], truncation=True, padding="max_length", max_length=512), batched=True, remove_columns=["sentence", "idx"]
    )

    tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
    tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    return tokenized_dataset

@asset(description= "Training dataset",group_name="training_pipeline",ins={"processed_datasets": AssetIn()})
def train_dataset(processed_datasets: datasets.DatasetDict):
    dataset = processed_datasets["train"].shuffle(seed=42).select(range(300))
    return Output(
        dataset,
        metadata={
            "len": MetadataValue.int(len(dataset))
        },
    )

@asset(description= "Validation dataset",group_name="training_pipeline",ins={"processed_datasets": AssetIn()})
def val_dataset(processed_datasets: datasets.DatasetDict):
    dataset = processed_datasets["validation"].shuffle(seed=42).select(range(100))
    return Output(
        dataset,
        metadata={
            "len": MetadataValue.int(len(dataset))
        }
    )
@asset(description="Test dataset",group_name="training_pipeline",ins={"processed_datasets": AssetIn()})
def test_dataset(processed_datasets: datasets.DatasetDict):
    dataset = processed_datasets["test"].shuffle(seed=42).select(range(100))
    return Output(
        dataset,
        metadata={
            "len": MetadataValue.int(len(dataset))
        }
    )

@asset(description="Save test dataset",group_name="training_pipeline",ins={"test_dataset": AssetIn()})
def save_test_dataset(test_dataset):
    # Initialize wandb
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'
    wandb.init(project="sentiment-analysis", name="test-dataset-upload")
    
    # Create a wandb artifact
    artifact = wandb.Artifact(
        name="test-dataset",
        type="dataset", 
        description="Test dataset for sentiment analysis evaluation"
    )
    
    # Save test dataset to a file
    test_dataset.save_to_disk("./test_dataset")
    
    # Add the test dataset directory to the artifact
    artifact.add_dir("./test_dataset")
    
    # Log the artifact to wandb
    wandb.log_artifact(artifact)
    
    # Close wandb run
    wandb.finish()
    
    return Output(
        value="Test dataset saved to wandb",
        metadata={
            "wandb_project": MetadataValue.text("sentiment-analysis"),
            "artifact_name": MetadataValue.text("test-dataset"),
            "dataset_size": MetadataValue.int(len(test_dataset))
        }
    )



@asset(description="Load test dataset",group_name="inference_pipeline")
def load_test_dataset():
    # Initialize wandb
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'
    wandb.init(project="sentiment-analysis", name="test-dataset-download")
    
    # Get the latest version of the test dataset artifact
    artifact = wandb.use_artifact('sentiment-analysis/test-dataset:latest')
    
    # Download the artifact
    artifact_dir = artifact.download()
    
    # Load the dataset from disk
    test_dataset = datasets.load_from_disk(artifact_dir)
    
    # Close wandb run
    wandb.finish()
    
    return Output(
        value=test_dataset,
        metadata={
            "wandb_project": MetadataValue.text("sentiment-analysis"),
            "artifact_name": MetadataValue.text("test-dataset"),
            "dataset_size": MetadataValue.int(len(test_dataset))
        }
    )


@asset(description="Upload inference results to wandb",group_name="inference_pipeline",ins={"inference_model": AssetIn()})
def load_inference_results_wandb(inference_model: pd.DataFrame):
    # Initialize wandb
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'
    wandb.init(project="sentiment-analysis", name="inference-results")
    
    # Create and log artifact
    artifact = wandb.Artifact(
        name="predictions", 
        type="predictions",
        description="Model predictions on test dataset"
    )
    
    # Save predictions to CSV and add to artifact
    predictions_path = "predictions.csv"
    inference_model.to_csv(predictions_path, index=False)
    artifact.add_file(predictions_path)
    
    # Log the artifact
    wandb.log_artifact(artifact)
    
    # Close wandb run
    wandb.finish()
    
    return Output(
        value="Predictions saved to wandb",
        metadata={
            "wandb_project": MetadataValue.text("sentiment-analysis"),
            "artifact_name": MetadataValue.text("predictions"),
            "num_predictions": MetadataValue.int(len(inference_model))
        }
    )
