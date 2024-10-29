import torchvision
from pathlib import Path
import wandb

def main():
    #Use the mounted volume path
    data_path = Path("/tmp/")
    
    # Download and save MNIST dataset to the mounted volume
    test_dataset = torchvision.datasets.MNIST(root=data_path, train=False, download=True,transform=torchvision.transforms.ToTensor())

if __name__ == "__main__":
    main()