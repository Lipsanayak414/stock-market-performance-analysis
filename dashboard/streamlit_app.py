import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

from src.predict import predict_price, predict_next_7_days

st.set_page_config(page_title="AI Stock Predictor", layout="wide")

st.title("📈 AI Stock Market Prediction Dashboard")

ticker = st.text_input("Enter Stock Ticker", "AAPL")

if ticker:

    # Download stock data
    data = yf.download(ticker, period="1y")

    # Detect currency
    ticker_obj = yf.Ticker(ticker)
    try:
        currency = ticker_obj.fast_info["currency"]
    except:
        currency = "USD"

    # Fix Yahoo Finance multi-index issue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data[["Open","High","Low","Close"]]

    if not data.empty:

        # Get prediction
        prediction = predict_price(ticker)

        # Get forecast
        forecast = predict_next_7_days(ticker)

        # Convert GBX / GBp (pence) → GBP
        if currency in ["GBX","GBp"]:
            prediction = prediction / 100
            forecast = forecast / 100
            currency = "GBP"

        # Currency symbols
        currency_symbols = {
            "USD": "$",
            "GBP": "£",
            "EUR": "€",
            "INR": "₹",
            "JPY": "¥",
            "CNY": "¥"
        }

        symbol = currency_symbols.get(currency, currency)

        # Display prediction
        st.markdown(f"## Predicted Price: {symbol}{prediction:.2f} (Next trading day)")

        # Prepare chart data
        chart_data = data.tail(70).copy()

        # Convert London prices from pence → pounds
        if currency == "GBP" and ticker.endswith(".L"):
            chart_data[["Open","High","Low","Close"]] = chart_data[["Open","High","Low","Close"]] / 100

        # Forecast dates
        last_date = chart_data.index[-1]

        future_dates = pd.date_range(
            start=last_date,
            periods=8,
            freq="B"
        )

        # Connect forecast smoothly to last candle
        forecast = list(forecast)
        last_real_price = chart_data["Close"].iloc[-1]
        forecast.insert(0, last_real_price)

        # Build chart
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=chart_data.index,
            open=chart_data["Open"],
            high=chart_data["High"],
            low=chart_data["Low"],
            close=chart_data["Close"],
            increasing_line_color="#00ff9f",
            decreasing_line_color="#ff4976",
            increasing_fillcolor="#00ff9f",
            decreasing_fillcolor="#ff4976",
            line_width=1.5,
            name="Price"
        ))

        fig.add_trace(go.Scatter(
            x=future_dates,
            y=forecast,
            mode="lines+markers",
            name="7 Day Forecast",
            line=dict(color="cyan", width=3)
        ))

        fig.update_layout(
            template="plotly_dark",
            height=900,
            xaxis_rangeslider_visible=False,
            title=f"{ticker} Price Chart with AI Forecast",
            xaxis_title="Date",
            yaxis_title=f"Price ({currency})"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"No stock data found for '{ticker}'")