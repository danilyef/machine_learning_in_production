import kfp
from kfp import dsl
from kfp.dsl import Dataset, Input, Model, Output
import torch
import torchvision


@dsl.component(base_image="python:3.11", packages_to_install=["torch", "torchvision"])
def load_training_data(dataset: Output[Dataset]):
    import torch
    import torchvision
    import shutil
    from pathlib import Path
    import os
    # Load MNIST dataset

    os.makedirs("./app/data", exist_ok=True)
    train_dataset_obj = torchvision.datasets.MNIST(
        root=Path("./app/data"),
        train=True,
        download=True,
        transform=torchvision.transforms.ToTensor(),
    )

    shutil.move(Path("./app/data"), dataset.path)


@dsl.component(base_image="python:3.11", packages_to_install=["torch", "torchvision"])
def train_model(dataset: Input[Dataset], model: Output[Model]):
    import torch
    import torchvision
    import shutil
    from pathlib import Path

    Path("./tmp").mkdir(exist_ok=True, parents=True)

    shutil.copytree(dataset.path, Path("./tmp/data"), dirs_exist_ok=True)

    # Load datasets
    train_dataset_obj = torchvision.datasets.MNIST(
        root=Path("./tmp/data"),
        train=True,
        download=False,
        transform=torchvision.transforms.ToTensor(),
    )

    # Define a simple neural network
    model_obj = torch.nn.Sequential(
        torch.nn.Flatten(),
        torch.nn.Linear(28 * 28, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10),
    )

    # Train the model
    optimizer = torch.optim.Adam(model_obj.parameters())
    criterion = torch.nn.CrossEntropyLoss()

    train_loader = torch.utils.data.DataLoader(
        train_dataset_obj, batch_size=64, shuffle=True
    )

    for batch_idx, batch in enumerate(train_loader):
        if batch_idx == 5:
            break
        inputs, targets = batch
        outputs = model_obj(inputs)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    Path("./tmp/model").mkdir(exist_ok=True, parents=True)
    # Save the trained model
    torch.save(model_obj, Path("./tmp/model/model.pth"))
    shutil.move(Path("./tmp/model/model.pth"), model.path)


@dsl.component(
    base_image="python:3.11", packages_to_install=["torch", "torchvision", "wandb"]
)
def save_trained_model(model: Input[Model]):
    import torch
    import shutil
    import wandb
    from pathlib import Path
    import os

    Path("./tmp/model").mkdir(exist_ok=True, parents=True)

    shutil.copy(model.path, Path("./tmp/model/model.pth"))

    # Load the trained model
    model_obj = torch.load(Path("./tmp/model/model.pth"))

    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = "0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384"

    # Initialize wandb
    wandb.init(project="mnist_training", name="model_upload")

    # Save and upload the model to wandb
    artifact = wandb.Artifact("mnist_model", type="model")
    with artifact.new_file("model.pth", mode="wb") as f:
        torch.save(model_obj, f)
    wandb.log_artifact(artifact)

    wandb.finish()


@dsl.pipeline(name="MNIST Training Pipeline")
def mnist_pipeline():
    load_data_task = load_training_data()
    train_model_task = train_model(
        dataset=load_data_task.outputs["dataset"],
    )
    save_model_task = save_trained_model(model=train_model_task.outputs["model"])


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler().compile(mnist_pipeline, "mnist_pipeline.yaml")

    client = kfp.Client()
    pipeline_info = client.upload_pipeline(
        pipeline_package_path="mnist_pipeline.yaml",
        pipeline_name="MNIST Training Pipeline",
        description="A pipeline to train a model on the MNIST dataset",
    )
