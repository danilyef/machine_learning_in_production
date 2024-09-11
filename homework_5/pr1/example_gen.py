import os
import pickle
import shutil
import pandas as pd
from datasets import Dataset, DatasetDict


class ExampleGen:
    def __init__(self, data_dir, metadata_dir, dataset_config, seed=None):
        """
        Initializes the ExampleGen class and loads dataset in predefined folder

        Args:
            data_dir (str): The directory path where the data is stored.
            cache_dir (str): The directory path for storing cache (default - None)
            seed (int): seting a seed for reproducability (default - None)
        """
        self.data_dir = data_dir
        self.metadata_dir = metadata_dir
        self.dataset_config = dataset_config
        self.cache_dir = os.path.join(metadata_dir, "cache")
        self.seed = seed
        self.dataset = None
        if len(os.listdir(data_dir)) != 0:
            self.df_pandas = pd.read_parquet(
                os.path.join(self.data_dir, "dataset.parquet")
            )

    def shuffle_dataset(self):
        """
        Shuffles the dataset.
        """
        self.dataset = self.dataset.shuffle()

    def preprocessing(self):
        # drop duplicates:
        if len(self.dataset_config["delete_duplicates"]) > 0:
            self.df_pandas = self.df_pandas.drop_duplicates(
                subset=self.dataset_config["delete_duplicates"]
            )

        # filter categories:
        categories_filtered = self.dataset_config["filter"]
        self.df_pandas = self.df_pandas[
            self.df_pandas["label"].isin(categories_filtered)
        ]

        # Join Subject and Category into one category
        self.df_pandas["text"] = (
            self.df_pandas["subject"] + " " + self.df_pandas["text"]
        )

        # Delete Unnecessary columns
        columns_to_delete = self.dataset_config.get("columns_to_delete")
        self.df_pandas.drop(columns=columns_to_delete, inplace=True)

        # Convert to Dataset Huggingface
        self.dataset = Dataset.from_pandas(self.df_pandas, preserve_index=False)

        # Encode grouped category as a label
        label_column = self.dataset_config.get("label_column")
        self.dataset = self.dataset.class_encode_column(label_column)

    def split_dataset(self):
        """
        Splits the dataset into training and evaluation subsets.

        """

        # Perform Dataset Split (stratified or not)
        stratified_column = self.dataset_config.get("stratified")
        split_ratio = self.dataset_config.get("split_ratio")
        if stratified_column != "":
            self.dataset = self.dataset.train_test_split(
                train_size=split_ratio,
                stratify_by_column=stratified_column,
                seed=self.seed,
            )
        else:
            self.dataset = self.dataset.train_test_split(
                train_size=split_ratio, seed=self.seed
            )

    def save_dataset(self):
        """
        Saves the current dataset to disk.

        Args:
            version (str): The version name for the saved dataset.
        """
        save_dir = os.path.join(self.metadata_dir, "dataset")
        os.makedirs(save_dir, exist_ok=True)
        self.dataset.save_to_disk(save_dir)
        if self.df_pandas is not None:
            self.df_pandas.to_pickle(os.path.join(save_dir, "dataset_pandas.pkl"))

        with open(os.path.join(save_dir, "dataset_config.pkl"), "wb") as fp:
            pickle.dump(self.dataset_config, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def load_dataset(self):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """

        load_dir = os.path.join(self.metadata_dir, "dataset")
        self.dataset = DatasetDict.load_from_disk(load_dir)

        with open(os.path.join(load_dir, "dataset_config.pkl"), "rb") as file:
            self.dataset_config = pickle.load(file)

    def cleanup(self):
        """
        Loads a previously saved version of the dataset.

        Args:
            version (str): The version name of the dataset to be loaded.
        """
        del self.dataset
        for item in os.listdir(self.cache_dir):
            item_path = os.path.join(self.cache_dir, item)

            # Check if the item is a file or a directory
            if os.path.isfile(item_path):
                # Remove the file
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Recursively remove the directory and its contents
                shutil.rmtree(item_path)
