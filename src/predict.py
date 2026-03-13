import numpy as np
import yfinance as yf
import os

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


# ---------------- Load trained model ----------------
model_path = os.path.join(os.path.dirname(__file__), "../models/lstm_model.h5")

if not os.path.exists(model_path):
    raise FileNotFoundError(
        "Model file not found. Please run: python3 src/train_model.py"
    )

model = load_model(model_path, compile=False)


# ---------------- Next-day prediction ----------------
def predict_price(ticker="AAPL"):

    df = yf.download(ticker, period="1y")

    close_prices = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(close_prices)

    last_60_days = scaled_data[-60:]

    X_test = np.reshape(last_60_days, (1, 60, 1))

    prediction = model.predict(X_test, verbose=0)

    predicted_price = scaler.inverse_transform(prediction)

    return round(float(predicted_price[0][0]), 2)


# ---------------- 7-day forecast ----------------
def predict_next_7_days(ticker="AAPL"):

    df = yf.download(ticker, period="1y")

    close_prices = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(close_prices)

    last_60_days = scaled_data[-60:]

    predictions = []

    for _ in range(7):

        X_test = np.reshape(last_60_days, (1, 60, 1))

        prediction = model.predict(X_test, verbose=0)

        predictions.append(prediction[0][0])

        last_60_days = np.append(last_60_days[1:], prediction)

    predictions = np.array(predictions).reshape(-1, 1)

    predictions = scaler.inverse_transform(predictions)

    predictions = predictions.flatten()

    # ---------------- Anchor forecast to last real price ----------------
    last_real_price = close_prices[-1][0]

    scale_factor = last_real_price / predictions[0]

    predictions = predictions * scale_factor

    return predictions