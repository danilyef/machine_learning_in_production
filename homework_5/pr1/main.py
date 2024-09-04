from utils import read_json_file, get_numeric_folders
import os
import wandb
from example_gen import ExampleGen
from schema import SchemaGeneration
from transform import Transform
from trainer import Training



# Paths to folders
metadata_dir = './metadata'
data_dir = './dataset'
pipeline_configs ='./pipeline_configs'
resources_dir = './resources'

# Read Configs
dataset_config = read_json_file(os.path.join(pipeline_configs,'dataset_config.json'))
transform_config = read_json_file(os.path.join(pipeline_configs,'transform_config.json'))
training_config = read_json_file(os.path.join(pipeline_configs,'training_config.json'))
data_type_config = read_json_file(os.path.join(pipeline_configs,'data_type_config.json'))


# Wandb Config
wandb.init(project="Project_my", entity="daniil-yefimov")

config = wandb.config
config.split_ratio = dataset_config['split_ratio']
config.tokenizer_name = transform_config['tokenizer_info']['tokenizer_name']
config.preprocessing_steps = transform_config['preprocessing_steps']
config.model = training_config['model']
config.batch_size = training_config['batch_size']
config.num_labels = training_config['num_labels']
config.epochs = training_config['epochs']
config.lr = training_config['lr']
config.weight_decay = training_config['weight_decay']

# Dataset Generation
example_gen = ExampleGen(data_dir = data_dir,metadata_dir = metadata_dir,dataset_config = dataset_config)
example_gen.preprocessing()
example_gen.shuffle_dataset()
example_gen.split_dataset()
example_gen.save_dataset()

# Schema Generation
schema = SchemaGeneration(metadata_dir = metadata_dir,data_type_config = data_type_config)
schema.generate_schema(example_gen.dataset)
schema.save_schema()

# Transform Data
transform_data = Transform(metadata_dir = metadata_dir, transform_config = transform_config)
transform_data.preprocess_fn(example_gen.dataset)
transform_data.save_transformed_dataset()

# Training
training = Training(metadata_dir=metadata_dir, tokenizer=transform_data.tokenizer, training_config=training_config)
training.train(transform_data.transformed_dataset, schema.schema)
training.save_model()


# Finish W&B logging
wandb.finish()





