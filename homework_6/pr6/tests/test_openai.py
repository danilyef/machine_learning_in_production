import pytest
from main import get_openai_response

@pytest.mark.parametrize("question,expected_answer", [
    ("Who was the first President of the United States?", "history"),
    ("What is the capital of France?", "geography"),
    ("What is the square root of 144?", "math"),
])
def test_openai_responses(question, expected_answer):
    response = get_openai_response(question)
    
    assert response is not None
    assert len(response) > 0
    assert expected_answer.lower() in response.lower()

def test_history_question():
    question = "What year did World War II end?"
    response = get_openai_response(question)
    
    assert "1945" in response

def test_math_question():
    question = "What is 10 multiplied by 7?"
    response = get_openai_response(question)
    
    assert "70" in response

def test_geography_question():
    question = "What is the largest country by land area in North America?"
    response = get_openai_response(question)
    
    assert "Canada" in response.lower()