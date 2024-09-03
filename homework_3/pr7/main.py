
from datasets import load_dataset
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import typer


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


