import psycopg2
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

# Get closing prices
cur.execute("""
SELECT close_price
FROM stock_prices
ORDER BY trade_date;
""")

rows = cur.fetchall()

# Convert data into a list
prices = [float(row[0]) for row in rows]

# Create training data
X = np.array(range(len(prices))).reshape(-1, 1)
y = np.array(prices)

# Train the model
model = LinearRegression()
model.fit(X, y)

# Predict tomorrow's closing price
tomorrow = np.array([[len(prices)]])
prediction = model.predict(tomorrow)

print("Today's Closing Price:", round(prices[-1], 2))
print("Predicted Tomorrow Price:", round(prediction[0], 2))

if prediction[0] > prices[-1]:
    print("🤖 AI Prediction: PRICE MAY GO UP")
else:
    print("🤖 AI Prediction: PRICE MAY GO DOWN")

cur.close()
conn.close()