import torch
import torchvision
from pathlib import Path

def run_inference():

    artifact_path = Path("/tmp/")

    # Load dataset from the mounted volume
    test_dataset_obj = torchvision.datasets.MNIST(root=artifact_path, train=False, download=False,
                                                   transform=torchvision.transforms.ToTensor())
    # Define model
    model_obj = torch.nn.Sequential(
        torch.nn.Flatten(),
        torch.nn.Linear(28*28, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10)
    )

    # Train the model
    optimizer = torch.optim.Adam(model_obj.parameters())
    criterion = torch.nn.CrossEntropyLoss()

    test_loader = torch.utils.data.DataLoader(test_dataset_obj, batch_size=64, shuffle=True)

    for batch_idx, batch in enumerate(test_loader):
        if batch_idx == 2:
            break
        inputs, targets = batch
        outputs = model_obj(inputs)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

if __name__ == "__main__":
    run_inference()