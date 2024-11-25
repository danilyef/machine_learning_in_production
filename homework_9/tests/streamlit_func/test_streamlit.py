import pytest
from pr1.func_st.utils import Model

@pytest.fixture
def model():
    return Model(
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
    probability = model.predict_proba(text)
    
    # Check if probability is a float
    assert isinstance(probability, float)
    
    # Check if probability is between 0 and 1
    assert 0 <= probability <= 1

def test_model_consistency(model):
    # Test if multiple predictions on same text are consistent
    text = "This is amazing!"
    first_prediction = model.predict(text)
    first_probability = model.predict_proba(text)
    
    # Test multiple times to ensure consistency
    for _ in range(3):
        assert model.predict(text) == first_prediction
        assert abs(model.predict_proba(text) - first_probability) < 1e-6