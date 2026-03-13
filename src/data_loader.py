import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker="AAPL", start="2015-01-01"):

    data = yf.download(ticker, start=start)

    data.reset_index(inplace=True)

    return data


if __name__ == "__main__":

    df = fetch_stock_data("AAPL")

    print(df.head())