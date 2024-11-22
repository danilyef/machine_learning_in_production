import pytest
from project.utils import Model

@pytest.fixture
def model():
    return Model(
        tokenizer_name="distilbert-base-uncased-finetuned-sst-2-english",
        model_name="distilbert-base-uncased-finetuned-sst-2-english"
    )

def test_model_prediction(model):
    # Test positive sentiment
    positive_text = "I love this movie!"
    assert model.predict(positive_text) == "POSITIVE"
    
    # Test negative sentiment
    negative_text = "I hate this movie!"
    assert model.predict(negative_text) == "NEGATIVE"

def test_model_probabilities(model):
    # Test probability output format
    text = "This is a test."
    probabilities = model.predict_proba(text)
    
    # Check if probabilities is a tuple/list of length 2
    assert len(probabilities) == 2
    
    # Check if probabilities sum to approximately 1
    assert abs(sum(probabilities) - 1.0) < 1e-6
    
    # Check if probabilities are between 0 and 1
    assert all(0 <= p <= 1 for p in probabilities)

def test_model_consistency(model):
    # Test if multiple predictions on same text are consistent
    text = "This is amazing!"
    first_prediction = model.predict(text)
    first_probabilities = model.predict_proba(text)
    
    # Test multiple times to ensure consistency
    for _ in range(3):
        assert model.predict(text) == first_prediction
        new_probabilities = model.predict_proba(text)
        assert all(abs(a - b) < 1e-6 for a, b in zip(first_probabilities, new_probabilities))