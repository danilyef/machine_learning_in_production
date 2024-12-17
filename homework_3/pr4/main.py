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
import matplotlib.pyplot as plt


# Prepare a sample dataset and model for benchmarking
def create_model_and_data():
    # Create a synthetic regression dataset with 100 features
    X, y = make_regression(n_samples=200000, n_features=100, noise=0.1, random_state=42)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.99, random_state=42)
    
    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, X_test

# Single inference task using the sklearn model
def inference_task(args):
    model, data = args
    time.sleep(0.005)
    # Simulate model inference (predicting the data)
    return model.predict(data)


def single_process_inference(model, batches):
    start_time = time.time()

    for batch in batches:
        inference_task((model, batch))

    elapsed_time = time.time() - start_time
    return elapsed_time


def multiple_process_inference(model, batches, num_processes=16):
    start_time = time.time()

    with mp.Pool(processes=num_processes) as pool:
        pool.map(inference_task, [(model, batch) for batch in batches])

    elapsed_time = time.time() - start_time
    return elapsed_time


if __name__ == '__main__':
    model, X_test = create_model_and_data()

    batch_sizes = [100, 2000]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    colors = ['#1f77b4', '#ff7f0e']  

    for i, batch_size in enumerate(batch_sizes):
        num_batches = len(X_test) // batch_size + (1 if len(X_test) % batch_size != 0 else 0)
        data_batches = np.array_split(X_test, num_batches)

        single_process_time = single_process_inference(model, data_batches)
        multiple_process_time = multiple_process_inference(model, data_batches)

        methods = ['Single Process', 'Multiple Processes']
        times = [single_process_time, multiple_process_time]

        ax = ax1 if i == 0 else ax2
        ax.bar(methods, times, color=colors)
        ax.set_title(f'Inference Time Comparison (Batch Size: {batch_size})')
        ax.set_xlabel('Method')
        ax.set_ylabel('Time (seconds)')

    plt.tight_layout()
    plt.savefig('inference_time_comparison.jpg')
    plt.close(fig)
