import nni
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


def get_params():
    params = {
        'features': 256,
        'lr': 0.001,
        'momentum': 0,
    }
    optimized_params = nni.get_next_parameter()
    params.update(optimized_params)
    return params


def get_data():
    training_data = datasets.FashionMNIST(root="data", train=True, download=True, transform=ToTensor())
    test_data = datasets.FashionMNIST(root="data", train=False, download=True, transform=ToTensor())
    return training_data, test_data


def get_dataloaders(training_data, test_data, batch_size=64):
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)
    return train_dataloader, test_dataloader


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class NeuralNetwork(nn.Module):
    def __init__(self, features):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, features),
            nn.ReLU(),
            nn.Linear(features, features),
            nn.ReLU(),
            nn.Linear(features, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device)
        pred = model(X)
        loss = loss_fn(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    return correct


def main():
    device = get_device()
    params = get_params()
    training_data, test_data = get_data()
    train_dataloader, test_dataloader = get_dataloaders(training_data, test_data)

    model = NeuralNetwork(params['features']).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=params['lr'], momentum=params['momentum'])

    epochs = 5
    for t in range(epochs):
        train(train_dataloader, model, loss_fn, optimizer)
        accuracy = test(test_dataloader, model, loss_fn)
        nni.report_intermediate_result(accuracy)
    nni.report_final_result(accuracy)


if __name__ == "__main__":
    main()