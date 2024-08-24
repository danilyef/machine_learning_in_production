import datasets
import pandas as pd
import torch
from torch.utils.data import IterableDataset, DataLoader


# Huggingface example
def create_data():
    return {
        'id': range(1, 1001),
        'name': [f'Person_{i}' for i in range(1, 1001)],
        'age': [20 + i % 60 for i in range(1000)],
        'score': [round(50 + 50 * torch.rand(1).item(), 2) for _ in range(1000)]
    }

def create_iterable_dataset(data):
    dataset = datasets.Dataset.from_pandas(pd.DataFrame(data))
    return dataset.to_iterable_dataset()


def main():
    data = create_data()
    dataset = create_iterable_dataset(data)
    for i, record in enumerate(dataset):
        print(f"Record {i + 1}:",record)
        if i == 9:
            break

main()


class StreamingDataset(IterableDataset):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for i in range(len(self.data['id'])):
            yield {key: self.data[key][i] for key in self.data}

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
