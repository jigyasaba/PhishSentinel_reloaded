from fastapi import FastAPI
from pydantic import BaseModel
from utils.predictor import predict_url
from utils.explainer import explain_url_result      
app = FastAPI(title="PhishSentinel API")


class URLInput(BaseModel):
    url: str


@app.get("/")
def home():
    return {"message": "PhishSentinel Running"}


@app.post("/predict-url")
def predict(data: URLInput):
    return predict_url(data.url)

@app.post("/explain-url")
def explain(data: URLInput):
    """
    Predict first, then explain result using Groq Llama
    """
    result = predict_url(data.url)

    explanation = explain_url_result(
        url=data.url,
        prediction=result["prediction"],
        confidence=result["confidence"],
        signals=result.get("signals", [])
    )

    return {
        "url": data.url,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "explanation": explanation
    }