import numpy as np
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import triton_python_backend_utils as pb_utils
import os

class TritonPythonModel:
    def initialize(self, args):
        # Model path and device setup
        model_path = args["model_repository"] + "/" + args["model_version"]  
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available, otherwise CPU

        # Load model and tokenizer
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        
        # Move model to the appropriate device (GPU/CPU)
        self.model.to(self.device)
    
        self.model.eval()  # Set model to evaluation mode

    def execute(self, requests):
        responses = []
        for request in requests:
            # Get input tensor (text_input)
            input_tensor = pb_utils.get_input_tensor_by_name(request, "text_input")
            input_text = input_tensor.as_numpy().astype(str).flatten().tolist()
            # Tokenize the input text
            inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)

            # Move the input tensors to the GPU if available
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)
            
            # Perform inference
            with torch.no_grad():
                logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits
            
            # Get predicted class IDs for each input in the batch
            predicted_class_ids = logits.argmax(dim=-1).tolist()

            
            # Create output tensor for the batch
            output_tensor = pb_utils.Tensor("label_output", np.array(predicted_class_ids, dtype=object))
            responses.append(pb_utils.InferenceResponse([output_tensor]))
        
        return responses
    
    def finalize(self):
        pass
