import pandas as pd


def create_features(df):

    # Moving averages
    df["MA10"] = df["Close"].rolling(window=10).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # Daily return
    df["Return"] = df["Close"].pct_change()

    # Volatility
    df["Volatility"] = df["Return"].rolling(window=10).std()

    # Remove missing values
    df.dropna(inplace=True)

    return df