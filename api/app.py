from fastapi import FastAPI
from src.predict import predict_price

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Stock Prediction API running"}


@app.get("/predict")
def predict(ticker: str):
    price = predict_price(ticker)

    return {
        "ticker": ticker,
        "predicted_price": price
    }