import json
import os
import spacy


def read_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data


def get_numeric_folders(directory):
    numeric_folders = [
        int(entry.name)
        for entry in os.scandir(directory)
        if entry.is_dir() and entry.name.isdigit()
    ]
    return sorted(numeric_folders)


# Remove Stop Words
def delete_stopwords(batch: dict, stop_words_nltk: set) -> dict:
    texts = []
    for example in batch["text"]:
        texts.append(
            " ".join(
                token
                for token in example.split()
                if token.lower() not in stop_words_nltk
            )
        )

    return {"text": texts}


# Lemmatization of words.
def lemma_string(batch: dict, nlp: spacy.language.Language) -> str:
    texts = []
    for example in batch["text"]:
        doc = nlp(example)
        texts.append(" ".join(token.lemma_ for token in doc if token.is_alpha))

    return {"text": texts}
