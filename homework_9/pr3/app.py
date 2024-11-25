from fastapi import FastAPI
from pydantic import BaseModel
from .utils import Model

model = Model(model_name='distilbert-base-uncased-finetuned-sst-2-english')

app = FastAPI()


class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    probability: float

class ProbabilityResponse(BaseModel):
    text: str 
    probability: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the sentiment analysis API"}

@app.post("/predict")
def predict_sentiment(request: SentimentRequest) -> SentimentResponse:
    label = model.predict(request.text)
    probability = model.predict_proba(request.text)
    return SentimentResponse(
        text=request.text,
        sentiment=label,
        probability=float(probability)
    )

@app.post("/probability")
def get_probability(request: SentimentRequest) -> ProbabilityResponse:
    probability = model.predict_proba(request.text)
    return ProbabilityResponse(
        text=request.text,
        probability=float(probability)
    )