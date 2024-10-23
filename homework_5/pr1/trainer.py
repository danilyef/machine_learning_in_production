import numpy as np
from transformers import (
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
import wandb
import pickle
import os
import pandas as pd
from utils import get_numeric_folders


class Training:
    def __init__(self, metadata_dir, tokenizer, training_config, seed=None):
        self.metadata_dir = metadata_dir
        self.model_dir = os.path.join(metadata_dir, "model")
        self.seed = seed
        self.version = len(get_numeric_folders(os.path.join(metadata_dir, "model"))) + 1

        self.training_config = training_config
        self.model = None
        self.tokenizer = tokenizer
        self.validation_result = None
        self.data_collator = DataCollatorWithPadding(
            tokenizer=tokenizer, return_tensors="pt"
        )

    def _predict_validation(self, transformed_test_dataset):
        pred = self.model.predict(transformed_test_dataset)
        pred = np.argmax(pred.logits, axis=1)
        return pred

    def train(self, transformed_data, schema):
        # load model
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.training_config["model"],
            num_labels=self.training_config["num_labels"],
            id2label=schema["mapping"]["int2str"],
            label2id=schema["mapping"]["str2int"],
        ).to("cuda")

        training_args = TrainingArguments(
            output_dir=os.path.join(self.model_dir, str(self.version)),
            learning_rate=self.training_config["lr"],
            per_device_train_batch_size=self.training_config["batch_size"],
            per_device_eval_batch_size=self.training_config["batch_size"],
            num_train_epochs=self.training_config["epochs"],
            weight_decay=self.training_config["weight_decay"],
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            save_total_limit=1,
            logging_dir="./logs",
            report_to="wandb",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=transformed_data["train"],
            eval_dataset=transformed_data["test"],
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
        )

        trainer.train()

        preds = trainer.predict(transformed_data["test"])
        self.validation_result = pd.DataFrame(
            {
                "label": preds.label_ids,
                "prediction": np.argmax(preds.predictions, axis=1),
                self.training_config["id_column"]: transformed_data["test"][
                    self.training_config["id_column"]
                ],
            }
        )

        # Log evaluation results
        eval_results = trainer.evaluate()
        wandb.log(eval_results)

    def save_model(self):
        """
        Saves the current dataset to disk.

        Args:
            version (str): The version name for the saved dataset.
        """

        # save dataset
        save_dir = os.path.join(self.metadata_dir, "model", str(self.version))
        os.makedirs(save_dir, exist_ok=True)

        checkpoints = [
            checkpoint
            for checkpoint in os.listdir(save_dir)
            if checkpoint.split("-")[0] == "checkpoint"
        ]

        if len(checkpoints) == 1:
            os.rename(os.path.join(save_dir, checkpoints[0]), "best_model")
        else:
            # Extract numbers from the strings and convert them to integers
            checkpoint_numbers = [int(cp.split("-")[1]) for cp in checkpoints]

            # Find the index of the checkpoint with the smaller number
            index_of_smaller_number = checkpoint_numbers.index(min(checkpoint_numbers))
            index_of_bigger_number = checkpoint_numbers.index(max(checkpoint_numbers))

            # Select the checkpoint with the smaller number
            best_checkpoint = checkpoints[index_of_smaller_number]
            other_checkpoint = checkpoints[index_of_bigger_number]

            # rename checkpoint to the best model
            os.rename(
                os.path.join(save_dir, best_checkpoint),
                os.path.join(save_dir, "best_model"),
            )
            if os.path.exists(os.path.join(save_dir, other_checkpoint)):
                # Remove the folder
                os.rmdir(os.path.join(save_dir, other_checkpoint))

        # save preprocessing steps
        with open(os.path.join(save_dir, "training_config.pkl"), "wb") as fp:
            pickle.dump(self.training_config, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self, version=1):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """

        load_dir = os.path.join(self.metadata_dir, "model", str(version))
        # load transformed dataset
        self.model = AutoModelForSequenceClassification.from_pretrained(load_dir)

        # load preprocessing steps
        with open(os.path.join(load_dir, "training_config.pkl"), "rb") as file:
            self.training_config = pickle.load(file)

    def load_tokenizer(self, version=1):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """
        load_dir = os.path.join(self.metadata_dir, "transform/tokenizer")
        self.tokenizer = AutoTokenizer.from_pretrained(load_dir)
