import spacy
import nltk
import pickle
import os
from transformers import AutoTokenizer
from nltk.corpus import stopwords
from datasets import DatasetDict
from utils import delete_stopwords, lemma_string

nltk.download("stopwords")


class Transform:
    def __init__(self, metadata_dir, transform_config, seed=None):
        self.transformed_dataset = None
        self.metadata_dir = metadata_dir
        self.transform_dir = os.path.join(metadata_dir, "transform")
        self.seed = seed
        self.transform_config = transform_config
        self.tokenizer = None
        self.nlp = spacy.load("de_core_news_lg")
        self.stop_words_nltk = set(stopwords.words("german"))

    def _get_training_corpus(self, dataset, variable_to_tokenize):
        dataset = dataset["train"]
        for start_idx in range(0, len(dataset), 1000):
            samples = dataset[start_idx : start_idx + 1000]
            yield samples[variable_to_tokenize]

    def _train_tokenizer(self, dataset, vocab_size, variable_to_tokenize):
        training_corpus = self._get_training_corpus(dataset, variable_to_tokenize)
        tokenizer = self.tokenizer.train_new_from_iterator(training_corpus, vocab_size)
        self.tokenizer = tokenizer
        del training_corpus

    def preprocess_fn(self, dataset):
        # Define transformation functions
        transformations = {
            "remove_stopwords": lambda batch: delete_stopwords(
                batch, self.stop_words_nltk
            ),
            "lemmatization": lambda batch: lemma_string(batch, self.nlp),
        }

        # Apply transformations
        transform_steps = self.transform_config["preprocessing_steps"]
        batch_size = self.transform_config.get("batch_size")

        for step in transform_steps:
            # if step != "lemmatization":
            transformation_fn = transformations.get(step)
            dataset = dataset.map(
                transformation_fn, batched=True, batch_size=batch_size
            )

        # Train Tokenizer
        tokenizer_name = self.transform_config["tokenizer_info"].get("tokenizer_name")
        tokenizer_training = bool(
            self.transform_config["tokenizer_info"].get("tokenizer_training")
        )
        vocab_size = self.transform_config["tokenizer_info"].get("vocab_size")
        max_length = self.transform_config["tokenizer_info"].get("max_length")
        truncation = bool(self.transform_config["tokenizer_info"].get("truncation"))
        variable_to_tokenize = self.transform_config["tokenizer_info"].get(
            "variable_to_tokenize"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        if tokenizer_training:
            self._train_tokenizer(dataset, vocab_size, variable_to_tokenize)

        # Tokenize
        tokenize = lambda example: self.tokenizer(
            example[variable_to_tokenize],
            truncation=truncation,
            max_length=max_length,
            return_tensors="pt",
            padding="max_length",
        )
        dataset = dataset.map(tokenize, batched=True, batch_size=batch_size)

        # Update instance variables
        self.transformed_dataset = dataset

    def save_transformed_dataset(self):
        """
        Saves the current dataset to disk.

        Args:
            version (str): The version name for the saved dataset.
        """

        # save dataset
        save_dir = os.path.join(self.metadata_dir, "transform")
        os.makedirs(save_dir, exist_ok=True)
        self.transformed_dataset.save_to_disk(save_dir)

        with open(os.path.join(save_dir, "transform_config.pkl"), "wb") as fp:
            pickle.dump(self.transform_config, fp, protocol=pickle.HIGHEST_PROTOCOL)

        # save tokenizer:
        self._save_tokenizer()

    def load_transformed_dataset(self):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """

        load_dir = os.path.join(self.metadata_dir, "transform")
        # load transformed dataset
        self.transformed_dataset = DatasetDict.load_from_disk(load_dir)

        # load preprocessing steps
        with open(os.path.join(load_dir, "transform_config.pkl"), "rb") as file:
            self.transform_config = pickle.load(file)

    def _save_tokenizer(self):
        """
        Saves the current dataset to disk.

        Args:
            version (str): The version name for the saved dataset.
        """

        # save dataset
        save_dir = os.path.join(self.metadata_dir, "transform/tokenizer")
        os.makedirs(save_dir, exist_ok=True)
        self.tokenizer.save_pretrained(save_dir)

    def _load_tokenizer(self):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """

        load_dir = os.path.join(self.metadata_dir, "transform/tokenizer")
        # load transformed dataset
        self.tokenizer = AutoTokenizer.from_pretrained(load_dir)
