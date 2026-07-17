import streamlit as st
import psycopg2
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from sklearn.linear_model import LinearRegression
import numpy as np

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(page_title="AI Trading Manager", layout="wide")

st.title("🤖 AI Trading Manager")
st.write("Professional Stock Analysis Dashboard")

# -----------------------------
# Stock Selector
# -----------------------------
st.write("📈 Stock: AAPL")
stock_symbol = "AAPL"

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

# -----------------------------
# Get Stock Data
# -----------------------------
cur.execute("""
SELECT trade_date, close_price
FROM stock_prices
WHERE symbol = %s
ORDER BY trade_date;
""", (stock_symbol,))

rows = cur.fetchall()

if len(rows) == 0:
    st.error(f"No data found for {stock_symbol}.")
    cur.close()
    conn.close()
    st.stop()

prices = [float(row[1]) for row in rows]
dates = [row[0] for row in rows]

price_series = pd.Series(prices)

# -----------------------------
# Technical Indicators
# -----------------------------
moving_average = sum(prices[-3:]) / 3
latest = prices[-1]

rsi = RSIIndicator(close=price_series, window=14)
rsi_value = rsi.rsi().iloc[-1]

macd = MACD(close=price_series)
macd_value = macd.macd().iloc[-1]
signal_value = macd.macd_signal().iloc[-1]

# -----------------------------
# Machine Learning Prediction
# -----------------------------
X = np.array(range(len(prices))).reshape(-1, 1)
y = np.array(prices)

model = LinearRegression()
model.fit(X, y)

prediction = model.predict([[len(prices)]])[0]

# -----------------------------
# Dashboard Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", f"${latest:.2f}")

with col2:
    st.metric("3-Day Average", f"${moving_average:.2f}")

with col3:
    st.metric("Tomorrow Prediction", f"${prediction:.2f}")

col4, col5 = st.columns(2)

with col4:
    st.metric("RSI", f"{rsi_value:.2f}")

with col5:
    st.metric("MACD", f"{macd_value:.2f}")

# -----------------------------
# AI Decision
# -----------------------------
if latest > moving_average and rsi_value < 70 and macd_value > signal_value:
    decision = "🟢 STRONG BUY"
elif latest < moving_average and rsi_value > 30 and macd_value < signal_value:
    decision = "🔴 STRONG SELL"
else:
    decision = "🟡 HOLD"

st.subheader("🤖 AI Decision")
st.success(decision)

# -----------------------------
# Price Chart
# -----------------------------
df = pd.DataFrame({
    "Date": dates,
    "Close Price": prices
})

st.subheader("📈 Stock Price Chart")
st.line_chart(df.set_index("Date"))

# -----------------------------
# Portfolio
# -----------------------------
st.subheader("💼 Portfolio")

cur.execute("""
SELECT symbol, shares, buy_price, buy_date
FROM portfolio;
""")

portfolio = cur.fetchall()

total_shares = 0
total_profit = 0
total_value = 0

if len(portfolio) == 0:
    st.info("No shares in portfolio.")
  else:
    for stock in portfolio:
        symbol, shares, buy_price, buy_date = stock

        shares = int(shares)
        buy_price = float(buy_price)

        current_value = latest * shares
        buy_value = buy_price * shares
        profit = current_value - buy_value

        total_shares += shares
        total_profit += profit
        total_value += current_value

        st.write(f"### 📈 {symbol}")
        st.write(f"**Shares:** {shares}")
        st.write(f"**Buy Price:** ${buy_price:.2f}")
        st.write(f"**Current Price:** ${latest:.2f}")
        st.write(f"**Current Value:** ${current_value:.2f}")

        if profit >= 0:
            st.success(f"Profit: +${profit:.2f}")
        else:
            st.error(f"Loss: ${profit:.2f}")

        st.write("---")

    st.metric("💼 Total Shares", total_shares)
    st.metric("💰 Portfolio Value", f"${total_value:.2f}")

    if total_profit >= 0:
        st.success(f"📈 Total Profit: +${total_profit:.2f}")
    else:
        st.error(f"📉 Total Loss: ${total_profit:.2f}")
# -----------------------------
# Close Connection
# -----------------------------
cur.close()
conn.close() 