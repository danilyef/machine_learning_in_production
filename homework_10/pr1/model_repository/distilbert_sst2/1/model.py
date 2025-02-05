
###################################################################################
import numpy as np
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import triton_python_backend_utils as pb_utils
import os


class TritonPythonModel:
    def initialize(self, args):
        model_path = args["model_repository"] + "/" + args["model_version"]  
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)




    def execute(self, requests):
        responses = []
        for request in requests:
            input_tensor = pb_utils.get_input_tensor_by_name(request, "text_input")
            input_text = input_tensor.as_numpy()[0].decode("utf-8")
            inputs = self.tokenizer(input_text, return_tensors="pt")
            with torch.no_grad():
                logits = self.model(**inputs).logits

            predicted_class_id = logits.argmax().item()
            output_label = self.model.config.id2label[predicted_class_id]


            output_tensor = pb_utils.Tensor("text_output", np.array([output_label.encode("utf-8")], dtype=object))
            responses.append(pb_utils.InferenceResponse([output_tensor]))
        return responses
    

    def finalize(self):
        pass


