import numpy as np
import torch
from transformers import MarianTokenizer, MarianMTModel
import triton_python_backend_utils as pb_utils
import os


class TritonPythonModel:
    def initialize(self, args):
        # Model path and device setup
        model_path = args["model_repository"] + "/" + args["model_version"]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available, otherwise CPU

        # Load model and tokenizer
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)
        self.model = MarianMTModel.from_pretrained(model_path)

        # Move model to the appropriate device (GPU/CPU)
        self.model.to(self.device)

        self.model.eval()  # Set model to evaluation mode

    def execute(self, requests):
        responses = []
        for request in requests:
            # Get input tensor (text_input)
            input_tensor = pb_utils.get_input_tensor_by_name(request, "german_text_input")
            input_text = input_tensor.as_numpy().astype(str).flatten().tolist()

            # Tokenize the input text
            inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

            # Move the input tensors to the GPU if available
            inputs = {key: value.to(self.device) for key, value in inputs.items()}

            # Perform inference
            with torch.no_grad():
                translated_tokens = self.model.generate(**inputs)

            # Get predicted class IDs for each input in the batch
            output_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)

            # Create output tensor for the batch
            output_tensor = pb_utils.Tensor("text_output", np.array(output_text, dtype=object).reshape(len(output_text),1))
            responses.append(pb_utils.InferenceResponse([output_tensor]))

        return responses

    def finalize(self):
        pass