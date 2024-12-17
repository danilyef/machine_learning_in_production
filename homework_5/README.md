# Homework 5: Training & Experiments 

## Tasks:

- PR1: Write code for training your model using the W&B experiment logger.
- PR2: Write code for conducting hyperparameter searches with W&B.
- PR3: Write code to create a model card for your model, which can be a simple markdown or utilize this toolset
- PR4: Write code for hyperparameter searches using NNI
- PR5: Write code for distributed training with PyTorch, Accelerate, and Ray.


### PR1: Note

All confige files and dataset to be inserted into the repo.

### PR5: Data Distributed Training

For the testing of 3 Frameworkds I used Lambda service and rented 1 machine with 4 GPUs.

**Pytorch DistributedDataParallel**

The main framework for distributed data training. The idea is, that mp.spawn to launch multiple processes for distributed training and in my case I launched 2 processes for 2 GPUs (forgot to change to 4 :( ).

It was pretty straightforward to implement, because there are a lot of guides. But for non-standard scenario configuration could me tricky.

**Accelerate Hugging Face**

Very easy to use. All you have to do is to wrap everything, that you want to distribute on several gpus into accelerate and prepare cnfig file (which is easily done in cmd by answering the questions about your use case).

**Ray DDP**

Unfortunatelly I had a problemn with running DDP on ray on Mnist dataset (for some uknown for me reason it was not working), that's why I used netword from a guide. From all of the framworks I like it the most, because it allows more customization, that accelerate, but at the samt time it's more easier to use than pytorch DDP..
