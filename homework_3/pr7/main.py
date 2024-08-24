'''
Before starting the script, create a virtual environment:

1. cd /path/to/your/project
2. python -m venv env
3. source env/bin/activate
5. pip install -r requirements.txt

After these steps start script from cmd:
5. python main.py
'''


from datasets import load_dataset
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import typer

"""
# Load the Rick and Morty Transcript dataset
dataset = load_dataset("Prarabdha/Rick_and_Morty_Transcript")

# Remove columns
dataset = dataset.remove_columns(['Unnamed: 0', 'episode no.'])

# Dataset to pandas
dataset = dataset['train'].to_pandas()


# Connect to the LanceDB database
db = lancedb.connect("/tmp/db")

# Initialize the sentence transformer model for embedding
model = get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5", device="cpu")


# This class defines the schema for storing quotes in LanceDB
class Quotes(LanceModel):
    # Field for the speaker's name
    speaker: str
    # Field for the dialogue text, which will be used as the source for embedding
    dialouge: str = model.SourceField()
    # Field for the vector embedding of the dialogue, with dimensions matching the model
    vector: Vector(model.ndims()) = model.VectorField()


# Create a table in the LanceDB database with the Quotes schema
table = db.create_table("rick_and_morty", schema=Quotes)

# Add the dataset to the table
table.add(dataset)

# Perform a semantic search query on the table
query = table.search("What is the purpose of existence?").limit(5).to_df()

# Print the query results
print(query)
"""

######################################

app = typer.Typer()

@app.command()
def create_index():
    dataset = load_dataset("Prarabdha/Rick_and_Morty_Transcript")
    dataset = dataset.remove_columns(['Unnamed: 0', 'episode no.'])

    # Select 100 records randomly
    sample_size = 2000
    dataset = dataset['train'].shuffle(seed=42).select(range(sample_size))

    # Create vector embeddings
    docs = [d['dialouge'] for d in dataset]

    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    embeddings = model.encode(docs, show_progress_bar=True)

    # create data for index
    data = [
        {
            "id": idx,
            "vector": embeddings[idx],
            "speaker": dataset[idx]['speaker'],
            "dialouge": dataset[idx]["dialouge"],
        }
        for idx in range(len(dataset))
    ]

    # Create index
    db = lancedb.connect("/tmp/db")
    table = db.create_table('Index', data=data, mode="overwrite")
    table.create_index()

    typer.echo("Index created successfully!")

@app.command()
def search_index(query: str, top_n: int = 2):
    db = lancedb.connect("/tmp/db")
    table = db.open_table('Index')
    
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    query_embedding = model.encode(query)

    results = table.search(query_embedding).limit(top_n).to_list()
    typer.echo('Results:')
    
    

    for result in results:

        typer.echo(result["speaker"])
        typer.echo(result["dialouge"])
        typer.echo()

if __name__ == "__main__":
    app()


# python main.py create-index
# python main.py search-index "Who are you?" --top-n 2