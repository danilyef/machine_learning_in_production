import datasets
import pandas as pd
import torch
from torch.utils.data import IterableDataset, DataLoader


# Huggingface example
def create_data(num_rows: int = 1000):
    return {
        'id': range(1, num_rows + 1),
        'name': [f'Person_{i}' for i in range(1, num_rows + 1)],
        'age': [20 + i % 60 for i in range(num_rows)],
        'score': [round(50 + 50 * torch.rand(1).item(), 2) for _ in range(num_rows)]
    }

def create_iterable_dataset(data):
    dataset = datasets.Dataset.from_pandas(pd.DataFrame(data))
    return dataset.to_iterable_dataset()


def main_iterable_dataset():
    # Create a dataset with 1000 rows
    data = create_data(num_rows=1000)
    # Convert the data to an iterable dataset
    dataset = create_iterable_dataset(data)
    # Iterate through the dataset and print the first 10 records
    for i, record in enumerate(dataset):
        print(f"Record {i + 1}:", record)
        if i == 9:
            break  # Stop after printing 10 records



class StreamingDataset(IterableDataset):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for i in range(len(self.data['id'])):
            yield {key: self.data[key][i] for key in self.data}


def main_streaming_dataset():
    # Create the data
    data = create_data()

    # Create the streaming dataset
    dataset = StreamingDataset(data)

    # Create a DataLoader for batching
    dataloader = DataLoader(dataset, batch_size=32)

    # Example
    for i, batch in enumerate(dataloader):
        print(batch)
        print('-' * 50) 
        if i == 1: 
            break


if __name__ == "__main__":
    main_iterable_dataset()
    print('-' * 50)
    main_streaming_dataset()
