# Homework 3: Storage and Processing

## Tasks:

- PR1: Write README instructions detailing how to deploy MinIO with the following options: Local, Docker, Kubernetes (K8S)-based.
- PR2: Develop a CRUD Python client for MinIO and accompany it with comprehensive tests.
- PR3: Write code to benchmark various Pandas formats in terms of data saving/loading, focusing on load time and save time.
- PR4: Create code to benchmark inference performance using single and multiple processes, and report the differences in time.
- PR5: Develop code for converting your dataset into the StreamingDataset format.
- PR6: Write code for transforming your dataset into a vector format, and utilize VectorDB for ingestion and querying.


### PR6: example

```bash
python main.py create-index
python main.py search-index "Who are you?" --top-n 2
```