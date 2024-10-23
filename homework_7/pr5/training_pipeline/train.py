import torch
import torchvision
import shutil
from pathlib import Path

def train_model():
    # Create temporary directories
    # Use the mounted volume path directly
    #data_path = Path("/opt/airflow/data")
    #model_path = Path("/opt/airflow/data/model")
    artifact_path = Path("/tmp/")
    #model_path = Path("/tmp/")
    #model_path.mkdir(exist_ok=True, parents=True)

    # Load dataset from the mounted volume
    train_dataset_obj = torchvision.datasets.MNIST(root=artifact_path, train=True, download=False,
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

    train_loader = torch.utils.data.DataLoader(train_dataset_obj, batch_size=64, shuffle=True)

    for batch_idx, batch in enumerate(train_loader):
        if batch_idx == 2:
            break
        inputs, targets = batch
        outputs = model_obj(inputs)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Save the trained model
    torch.save(model_obj.state_dict(), artifact_path / "model.pth")
    print(f"Model saved to {artifact_path / 'model.pth'}")

if __name__ == "__main__":
    train_model()