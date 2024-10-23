import pytest
from project.model import TextClassifier


@pytest.fixture
def classifier():
    return TextClassifier()


def test_predict(classifier):
    text = "This movie is great!"

    assert classifier.predict(text) in ["POSITIVE", "NEGATIVE"]


def test_predict_proba(classifier):
    text = "The weather is nice today."
    probability = classifier.predict_proba(text)

    assert 0 <= probability <= 1


def test_initialization():
    custom_model = "distilbert-base-uncased"
    classifier = TextClassifier(model_name=custom_model)

    assert classifier.tokenizer.name_or_path == custom_model
    assert classifier.model.name_or_path == custom_model


def test_input_handling(classifier):
    empty_text = ""
    long_text = "This is a very long text " * 100

    assert classifier.predict(empty_text) in ["POSITIVE", "NEGATIVE"]
    assert classifier.predict(long_text) in ["POSITIVE", "NEGATIVE"]
