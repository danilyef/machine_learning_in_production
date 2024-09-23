import kfp
from kfp import dsl
import torch
import torchvision

@dsl.component
def load_training_data():
    # Load MNIST dataset
    train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True,
                                               transform=torchvision.transforms.ToTensor())
    return train_dataset


@dsl.component
def train_model(train_dataset: torchvision.datasets.MNIST):
    # Define a simple neural network
    model = torch.nn.Sequential(
        torch.nn.Flatten(),
        torch.nn.Linear(28*28, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10)
    )
    
    # Train the model
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    for epoch in range(1):  # Train for 1 epochs
        for batch in train_loader:
            inputs, targets = batch
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    return model

@dsl.component
def save_trained_model(model: torch.nn.Module):
    # Save the trained model
    torch.save(model.state_dict(), 'mnist_model.pth')

@dsl.pipeline(name='MNIST Training Pipeline')
def mnist_pipeline():
    load_data_task = load_training_data()
    train_model_task = train_model(load_data_task.output)
    save_model_task = save_trained_model(train_model_task.output)


if __name__ == '__main__':
    # Compile the pipeline
    kfp.compiler.Compiler().compile(mnist_pipeline, 'mnist_pipeline.yaml')