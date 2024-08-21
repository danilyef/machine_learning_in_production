'''
Before starting the script, create a virtual environment:

1. cd /path/to/your/project
2. python -m venv env
3. source env/bin/activate
4. pip install -r requirements.txt

After these steps start script from cmd:
5. python main.py
'''
import time
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import numpy as np



# Prepare a sample dataset and model for benchmarking
def create_model_and_data():
    # Create a synthetic regression dataset with 100 features
    X, y = make_regression(n_samples=5000000, n_features=100, noise=0.1, random_state=42)
    
    # Split into training and testing setsx
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, X_test

# Single inference task using the sklearn model
def inference_task(model, data):
    # Simulate model inference (predicting the data)
    return model.predict(data)




def single_process_inference(model,batches):
    start_time = time.time()

    for batch in batches:
        inference_task(model,batch)


    elapsed_time = time.time() - start_time
    return elapsed_time




def multiple_process_inference(model,batches,num_processes = 4):
    
    start_time = time.time()

    with mp.Pool(processes=num_processes) as pool:
        pool.starmap(inference_task,[(model, batch) for batch in batches])
    

    elapsed_time = time.time() - start_time
    return elapsed_time

if __name__ == '__main__': 
    model, X_test  = create_model_and_data()

    batch_size = 128
    num_batches = len(X_test) // batch_size + (1 if len(X_test) % batch_size != 0 else 0)

    data_batches = np.array_split(X_test, num_batches)

    print(single_process_inference(model,data_batches))
    print(multiple_process_inference(model,data_batches))