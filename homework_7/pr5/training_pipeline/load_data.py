import torchvision
from pathlib import Path

def main():
    #Use the mounted volume path
    #data_path = Path("/opt/airflow/data")
    #data_path.mkdir(parents=True, exist_ok=True)
    data_path = Path("/tmp/")

    # Download and save MNIST dataset to the mounted volume
    train_dataset = torchvision.datasets.MNIST(root=data_path, train=True, download=True,transform=torchvision.transforms.ToTensor())
    test_dataset = torchvision.datasets.MNIST(root=data_path, train=False, download=True,transform=torchvision.transforms.ToTensor())

    print(f"MNIST dataset downloaded and saved to {data_path}")
    print(f"Number of training samples: {len(train_dataset)}")
    print(f"Number of test samples: {len(test_dataset)}")
    #print("Hello World")

if __name__ == "__main__":
    main()