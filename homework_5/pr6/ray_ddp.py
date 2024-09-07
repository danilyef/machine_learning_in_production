import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
import ray
from ray import train
from ray.train import Trainer

# Define a simple CNN model
class CNN_Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        self.act = F.relu

    def forward(self, x):
        x = self.act(self.conv1(x))
        x = self.act(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.act(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


# Define the training function
def train_func(config):
    # Set up data loading
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    dataset = datasets.MNIST('data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=config["batch_size"])

    # Create model, optimizer, and loss function
    model = CNN_Model()
    optimizer = optim.Adadelta(model.parameters(), lr=config["lr"])
    criterion = nn.CrossEntropyLoss()

    # Wrap the model with DistributedDataParallel
    model = train.torch.prepare_model(model)

    for epoch in range(config["num_epochs"]):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % 10 == 0:
                print(f'Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item()}')

        # Report metrics to Ray Tune
        train.report({"loss": loss.item()})

def main():
    # Initialize Ray
    ray.init()

    # Configure the training
    config = {
        "lr": 1.0,
        "batch_size": 64,
        "num_epochs": 5,
    }

    # Create a Trainer
    trainer = Trainer(backend="torch", num_workers=4)

    # Start distributed training
    result = trainer.run(
        train_func,
        config=config,
        callbacks=[],
    )

    print("Training completed!")

if __name__ == "__main__":
    main()