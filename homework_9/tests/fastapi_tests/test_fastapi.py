from fastapi.testclient import TestClient
from pr3.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the sentiment analysis API"}

def test_predict_sentiment():
    # Test with positive text
    response = client.post(
        "/predict",
        json={"text": "I love this movie!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "sentiment" in data
    assert "probability" in data
    assert data["text"] == "I love this movie!"
    assert isinstance(data["sentiment"], str)
    assert isinstance(data["probability"], float)
    assert 0 <= data["probability"] <= 1

    # Test with negative text
    response = client.post(
        "/predict",
        json={"text": "I hate this movie!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "sentiment" in data
    assert "probability" in data
    assert data["text"] == "I hate this movie!"
    assert isinstance(data["sentiment"], str)
    assert isinstance(data["probability"], float)
    assert 0 <= data["probability"] <= 1

def test_get_probability():
    response = client.post(
        "/probability",
        json={"text": "This is a test message"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "probability" in data
    assert data["text"] == "This is a test message"
    assert isinstance(data["probability"], float)
    assert 0 <= data["probability"] <= 1

def test_invalid_request():
    # Test missing text field
    response = client.post(
        "/predict",
        json={}
    )
    assert response.status_code == 422

    response = client.post(
        "/probability",
        json={}
    )
    assert response.status_code == 422