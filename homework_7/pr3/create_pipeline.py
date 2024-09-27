import kfp
from kfp import dsl
from kfp.dsl import Dataset, Input, Model, Output
import torch
import torchvision


@dsl.component(base_image='python:3.11', packages_to_install=['torch', 'torchvision'])
def load_inference_data(dataset: Output[Dataset]):
    import torch
    import torchvision
    import shutil
    from pathlib import Path
    import os
    # Load MNIST dataset

    os.makedirs('./app/data',exist_ok=True)
    test_dataset_obj = torchvision.datasets.MNIST(root=Path("./app/data"), train=False, download=True,
                                                   transform=torchvision.transforms.ToTensor())
    shutil.move(Path("./app/data"), dataset.path)


@dsl.component(base_image='python:3.11', packages_to_install=['torch', 'torchvision','wandb'])
def load_trained_model(model: Output[Model]):
    import torch
    import torchvision
    import shutil
    from pathlib import Path
    import wandb
    import os

   
    Path("./tmp/model").mkdir(exist_ok=True,parents=True)


    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'

    # Initialize wandb
    wandb.init(project="mnist_training", name="model_download")

    # Download the model from wandb
    artifact = wandb.use_artifact('mnist_model:latest', type='model')
    model_dir = artifact.download(root=Path("./tmp/model"))

    wandb.finish()

    shutil.move(Path("./tmp/model/model.pth"), model.path)
   

@dsl.component(base_image='python:3.11', packages_to_install=['torch', 'torchvision','wandb'])
def run_inference(model: Input[Model], dataset: Input[Dataset], result: Output[Dataset]):
    import torch
    import torchvision
    import shutil
    from pathlib import Path
    import os

    # Load datasets
    Path("./tmp").mkdir(exist_ok=True,parents=True)
    shutil.copytree(dataset.path, Path("./tmp/data"), dirs_exist_ok=True)

    test_dataset_obj = torchvision.datasets.MNIST(root=Path("./tmp/data"), train=False, download=False,
                                                   transform=torchvision.transforms.ToTensor())
    test_loader = torch.utils.data.DataLoader(test_dataset_obj, batch_size=64, shuffle=True)
    
    # Load model
    Path("./tmp/model").mkdir(exist_ok=True,parents=True)
    shutil.copy(model.path, Path("./tmp/model/model.pth"))

    # Load the trained model
    model = torch.load(Path("./tmp/model/model.pth"))
    model.eval()

    total_correct = 0
    total_samples = 0

    with torch.no_grad():  # Disable gradient computation
        for batch_idx, (inputs, targets) in enumerate(test_loader):
            if batch_idx == 5:
                break
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total_samples += targets.size(0)
            total_correct += (predicted == targets).sum().item()

    accuracy = total_correct / total_samples
    print(f"Test Accuracy: {accuracy:.4f}")

    # Create result directory
    result_dir = Path("./tmp/result")
    result_dir.mkdir(exist_ok=True, parents=True)

    # Write accuracy to a text file
    with open(result_dir / "accuracy.txt", "w") as f:
        f.write(f"Test Accuracy: {accuracy:.4f}")
    # Move the result to the output
    shutil.move(result_dir, result.path)

@dsl.component(base_image='python:3.11', packages_to_install=['torch', 'torchvision'])
def save_inference_results(result: Input[Dataset]):
    import torch
    import shutil
    import wandb
    from pathlib import Path
    import os

    Path("./tmp/result").mkdir(exist_ok=True,parents=True)

    shutil.copytree(result.path, Path("./tmp/result"), dirs_exist_ok=True)

    with open(Path("./tmp/result/accuracy.txt"), "r") as f:
        accuracy = f.read()

    print(accuracy)

    # Set the Weights & Biases API key
    os.environ["WANDB_API_KEY"] = '0935cbeb7aa9b75ee50eb2235ec860d7ecf8e384'

    # Initialize wandb
    wandb.init(project="mnist_inference", name="inference_results")

    # Log the existing accuracy file to wandb
    artifact = wandb.Artifact('mnist_inference', type='model')
    artifact.add_file(Path("./tmp/result/accuracy.txt"))
    wandb.log_artifact(artifact)
    wandb.finish()

@dsl.pipeline(name='MNIST  Inference Pipeline')
def mnist_pipeline():
    load_data_task = load_inference_data()
    load_model_task = load_trained_model()
    run_inference_task = run_inference(
        model=load_model_task.outputs['model'],
        dataset=load_data_task.outputs['dataset'],
    )
    
    save_model_task = save_inference_results(result=run_inference_task.outputs['result'])


if __name__ == '__main__':
    # Compile the pipeline
    kfp.compiler.Compiler().compile(mnist_pipeline, 'mnist_inference_pipeline.yaml')

    client = kfp.Client()
    pipeline_info = client.upload_pipeline(
        pipeline_package_path='mnist_inference_pipeline.yaml',
        pipeline_name='MNIST Inference Pipeline 3',
        description='A pipeline to train a model on the MNIST dataset'
    )



'''
 # Train the model
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()

    test_loader = torch.utils.data.DataLoader(test_dataset_obj, batch_size=64, shuffle=True)
    
    model.eval()  # Set the model to evaluation mode
    total_correct = 0
    total_samples = 0

    with torch.no_grad():  # Disable gradient computation
        for batch_idx, (inputs, targets) in enumerate(test_loader):
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total_samples += targets.size(0)
            total_correct += (predicted == targets).sum().item()

    accuracy = total_correct / total_samples
    print(f"Test Accuracy: {accuracy:.4f}")

    
    
    Path("./tmp/model").mkdir(exist_ok=True,parents=True)
    # Save the trained model




'''