from locust import HttpUser, task, between
import json

class TritonEnsembleInferenceUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests, can be adjusted

    @task
    def query_ensemble_model(self):
        # URL for Triton Inference Server's ensemble model inference API
        api_url = "/v2/models/ensemble_model/infer"  # Adjust to your ensemble model name

        # Define the input data for the ensemble model (German text input)
        input_data = {
            "inputs": [
                {
                    "name": "german_text_input",  # The name of the input tensor
                    "shape": [1,1],  # The shape should be a list of strings, can also be [-1] for dynamic input
                    "datatype": "BYTES",  # The datatype for string inputs
                    "data": ["Wie geht es dir?"]  # Example German text input for translation
                }
            ]
        }

        # Send the POST request to the ensemble model's inference endpoint
        with self.client.post(api_url, json=input_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")

