import numpy as np
import tritonclient.grpc as grpcclient

client = grpcclient.InferenceServerClient(url="localhost:8001")


batch_texts = ["Wie geht es dir?", "Es geht mir gut"]
batch_texts_inputs = np.array(batch_texts, dtype=object).reshape(len(batch_texts),1)

inputs = grpcclient.InferInput("german_text_input", batch_texts_inputs.shape, "BYTES")
inputs.set_data_from_numpy(batch_texts_inputs)

outputs = grpcclient.InferRequestedOutput("label_output")
response = client.infer(model_name="ensemble_model", inputs = [inputs], outputs=[outputs],model_version="1")
output_data = response.as_numpy("label_output")


print(output_data)