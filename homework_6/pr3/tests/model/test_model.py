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


# Behavior tests
@pytest.mark.parametrize("text_1, text_2, expected_sentiment", [
    ("This movie is great!", "This movie is blody awesome!", "POSITIVE"),
    ("This movie is terrible!", "This movie is disappointing!", "NEGATIVE"),
    ("Movie delivers an exciting and refreshing take on its genre, featuring compelling characters, sharp dialogue, and a plot that keeps you hooked, all wrapped in stunning visuals and a dynamic soundtrack.",
     "Movie is is disgustingly good, with outrageously captivating performances and a ridiculously well-executed plot that grabs you from the start. The visuals are absurdly stunning, and the soundtrack is almost unfairly perfect, making it an insanely enjoyable watch from beginning to end.",
     "POSITIVE")
])
def test_invariance(classifier, text_1, text_2, expected_sentiment):
    assert classifier.predict(text_1) == expected_sentiment
    assert classifier.predict(text_1) == classifier.predict(text_2)


@pytest.mark.parametrize("text_1, text_2", [
    ("Movie is a visually stunning and emotionally gripping film, with outstanding performances and a well-crafted story that keeps you engaged from start to finish.",
     "Movie  is visually impressive but falls flat with a lackluster story and underwhelming performances, making it hard to stay engaged from start to finish."),
    ("Movie is an engaging and heartwarming film, with strong performances and a captivating story that draws you in, beautifully blending emotion, humor, and stunning visuals for a thoroughly enjoyable experience.",
     "Movie tries to be engaging, but weak performances and a disjointed story leave it feeling flat, lacking the emotional depth or humor needed to make it truly enjoyable.")
])
def test_directional(classifier, text_1, text_2):
    assert classifier.predict(text_1) == "POSITIVE"
    assert classifier.predict(text_2) == "NEGATIVE"


@pytest.mark.parametrize("text, expected_sentiment", [
    ("This movie is great!", "POSITIVE"),
    ("I hate this movie!", "NEGATIVE")
])
def test_minimum_functionality(classifier, text, expected_sentiment):
    assert classifier.predict(text) == expected_sentiment

