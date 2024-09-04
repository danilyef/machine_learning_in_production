import pickle
import os
import pandas as pd
from utils import get_numeric_folders


class SchemaGeneration:
    def __init__(self,metadata_dir,data_type_config,seed = None):
        self.schema = {}
        self.metadata_dir = metadata_dir
        self.schema_dir = os.path.join(metadata_dir,'schema')
        self.seed = seed
        self.data_type_config = data_type_config
        self.version = len(get_numeric_folders(os.path.join(metadata_dir,'schema'))) + 1
    
    
    
    
    def _create_mapping(self,dataset):
        num_class = dataset['train'].features['label'].num_classes
        names = dataset['train'].features['label'].int2str(range(0,num_class))
        idx = list(range(0,num_class))

        mapping = {}
        mapping['str2int'] = dict(zip(names,idx))
        mapping['int2str'] = dict(zip(idx,names))
        return mapping

    def generate_schema(self,examples):
        mapping = self._create_mapping(examples)
        reference_df = pd.DataFrame(examples['train'])
        self.schema = {'data_types':self.data_type_config,
                       'mapping': mapping,
                      'reference_df': reference_df
                      }
        
    def save_schema(self):

        save_dir = os.path.join(self.schema_dir,str(self.version))
        os.makedirs(save_dir, exist_ok=True)

        with open(os.path.join(save_dir,'schema.pkl'), 'wb') as fp:
            pickle.dump(self.schema, fp, protocol=pickle.HIGHEST_PROTOCOL)
            
        with open(os.path.join(save_dir,'data_type_config.pkl'), 'wb') as fp:
            pickle.dump(self.schema, fp, protocol=pickle.HIGHEST_PROTOCOL)


    def load_schema(self,version = 'latest'):

        if version == 'latest':
            version = max(get_numeric_folders(os.path.join(self.metadata_dir,'schema')))

        load_dir = os.path.join(self.schema_dir ,str(version))
        
        with open(os.path.join(load_dir,'schema.pkl'), 'rb') as file:
            self.schema = pickle.load(file)

        with open(os.path.join(load_dir,'data_type_config.pkl'), 'rb') as file:
            self.data_type_config = pickle.load(file)
