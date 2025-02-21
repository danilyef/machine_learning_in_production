import tritonclient.http as httpclient
import numpy as np
import time

# URL and model settings
TRITON_URL = "localhost:8000"  # Change to your Triton server's address
MODEL_NAME = "distilbert_sst2"  # Replace with your model name
MODEL_VERSION = "1"  # Replace with your model version

# Function to send requests to Triton
def main():
    # Prepare some dummy text inputs (we'll send 50 requests with 8 items per request)
    total_requests = 50
    batch_size = 8

    # Sample text input data (adjust the content if needed)
    texts = [
        "This is a test sentence.",
        "Another example sentence.",
        "Triton Inference Server is great.",
        "Let's see how this performs.",
        "I love working with AI.",
        "Natural Language Processing is fascinating.",
        "Deep learning is the future.",
        "Let's try batch processing.",
        "AI will revolutionize industries.",
        "Machine learning is an exciting field.",
        "OpenAI makes some amazing models.",
        "Triton supports multiple backends.",
        "Natural language understanding is key.",
        "Large language models are powerful.",
        "The future is powered by AI.",
        "Deep neural networks are complex.",
        "Training large models requires resources.",
        "Data is key to machine learning success.",
        "Reinforcement learning is an exciting domain.",
        "AI can assist in many fields.",
        "AI research is rapidly advancing.",
        "Language models can generate text.",
        "Ethics in AI is a growing concern.",
        "AI can help with automation.",
        "Natural language processing has many applications.",
        "The potential of AI is huge.",
        "AI has applications in healthcare.",
        "GPT-3 is a powerful language model.",
        "Transformer models have revolutionized NLP.",
        "Text classification is a common NLP task.",
        "Deep learning is a subset of machine learning.",
        "AI will change the way we live.",
        "AI-driven solutions are improving efficiency.",
        "Machine translation is a popular NLP task.",
        "AI is transforming the tech industry.",
        "Natural language generation can be creative.",
        "AI systems need to be explainable.",
        "AI is being integrated into everyday life.",
        "AI will impact all sectors of the economy.",
        "Conversational AI is becoming more advanced.",
        "AI models are getting larger and more powerful.",
        "The future of AI is bright.",
        "AI models require large datasets for training.",
        "Supervised learning is a popular technique.",
        "Unsupervised learning helps in pattern discovery.",
        "Reinforcement learning can teach AI agents.",
        "AI can be used in autonomous vehicles.",
        "AI can be used in agriculture.",
        "The ethical use of AI is important.",
        "AI can help in decision-making.",
        "AI is revolutionizing finance."
    ]

    texts = texts * 8
    # Prepare the Triton client
    with httpclient.InferenceServerClient(url=TRITON_URL) as client:
        # Loop through the number of requests (50 requests, batch size 8 each)
        start_time = time.time()
        for request_idx in range(total_requests):

            batch_texts = texts[request_idx * batch_size : (request_idx + 1) * batch_size]
            batch_texts_inputs = np.array(batch_texts, dtype=object).reshape(len(batch_texts),1)
            
            inputs = httpclient.InferInput("text_input", batch_texts_inputs.shape, "BYTES")
            inputs.set_data_from_numpy(batch_texts_inputs)
            
            outputs = httpclient.InferRequestedOutput("label_output")

            response = client.infer(MODEL_NAME, [inputs], outputs=[outputs],model_version=MODEL_VERSION)
            
            output_data = response.as_numpy("label_output")
        
        end_time = time.time()
        print(f"Request {request_idx + 1} - Inference time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()
