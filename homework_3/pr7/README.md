# PR7: Write code for transforming your dataset into a vector format, and utilize VectorDB for ingestion and querying.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/danilyef/machine_learning_in_production.git
   cd homework_3/pr7
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the main script:
   ```
   python main.py create-index
   python main.py search-index "Who are you?" --top-n 2
   ```