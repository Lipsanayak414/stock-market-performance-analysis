import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from data_loader import fetch_stock_data
from feature_engineering import create_features


# Load data
df = fetch_stock_data("AAPL")

# Create features
df = create_features(df)

# Use closing price
data = df["Close"].values.reshape(-1,1)

# Scale data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

X = []
y = []

for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i])
    y.append(scaled_data[i])

X = np.array(X)
y = np.array(y)

# Build LSTM model
model = Sequential()

model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mse")

# Train model
model.fit(X, y, epochs=5, batch_size=32)

# Save model
model.save("../models/lstm_model.h5")

print("Model training complete and saved.")