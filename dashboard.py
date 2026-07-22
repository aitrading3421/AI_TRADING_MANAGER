import streamlit as st
import psycopg2
import pandas as pd
import numpy as np
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
from sklearn.linear_model import LinearRegression

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="AI Trading Manager", layout="wide")

st.title("🤖 AI Trading Manager")
st.write("Professional AI Paper Trading Dashboard")

# -----------------------------
# DATABASE CONNECTION
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
# ACCOUNT BALANCE
# -----------------------------
cur.execute("SELECT balance FROM account LIMIT 1;")
row = cur.fetchone()

if row:
    balance = float(row[0])
else:
    balance = 0.0

st.subheader("💰 Paper Trading Account")
st.metric("Account Balance", f"${balance:,.2f}")

# -----------------------------
# STOCK
# -----------------------------
stock_symbol = "AAPL"

cur.execute("""
SELECT trade_date, close_price
FROM stock_prices
WHERE symbol=%s
ORDER BY trade_date;
""", (stock_symbol,))

rows = cur.fetchall()

if not rows:
    st.error("No stock data found.")
    st.stop()

dates = [r[0] for r in rows]
prices = [float(r[1]) for r in rows]

price_series = pd.Series(prices)

latest = prices[-1]
moving_average = sum(prices[-3:]) / 3
# -----------------------------
# TECHNICAL INDICATORS
# -----------------------------
rsi = RSIIndicator(close=price_series, window=14)
rsi_value = float(rsi.rsi().iloc[-1])

macd = MACD(close=price_series)
macd_value = float(macd.macd().iloc[-1])
signal_value = float(macd.macd_signal().iloc[-1])

# -----------------------------
# MACHINE LEARNING PREDICTION
# -----------------------------
X = np.arange(len(prices)).reshape(-1, 1)
y = np.array(prices)

model = LinearRegression()
model.fit(X, y)

prediction = float(model.predict([[len(prices)]])[0])

# -----------------------------
# DASHBOARD METRICS
# -----------------------------
st.subheader("📊 Market Analysis")

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
# AI DECISION
# -----------------------------
if latest > moving_average and rsi_value < 70 and macd_value > signal_value:
    decision = "🟢 STRONG BUY"
elif latest < moving_average and rsi_value > 30 and macd_value < signal_value:
    decision = "🔴 STRONG SELL"
else:
    decision = "🟡 HOLD"

st.subheader("🤖 AI Trading Decision")
st.success(decision)
st.subheader("📌 Execute Paper Trade")

shares = st.number_input("Shares", min_value=1, value=10)

if st.button("Execute AI Trade"):

    if "BUY" in decision:

        total = latest * shares

        cur.execute("""
        INSERT INTO portfolio(symbol, shares, buy_price, buy_date)
        VALUES(%s,%s,%s,NOW())
        """,(stock_symbol,shares,latest))

        cur.execute("""
        INSERT INTO trade_history(symbol,action,shares,price,total)
        VALUES(%s,%s,%s,%s,%s)
        """,(stock_symbol,"BUY",shares,latest,total))

        conn.commit()

        st.success("BUY Trade Saved!")

    elif "SELL" in decision:

        total = latest * shares

        cur.execute("""
        INSERT INTO trade_history(symbol,action,shares,price,total)
        VALUES(%s,%s,%s,%s,%s)
        """,(stock_symbol,"SELL",shares,latest,total))

        conn.commit()

        st.success("SELL Trade Saved!")

    else:

        st.warning("AI says HOLD")
# -----------------------------
# PRICE CHART
# -----------------------------
st.subheader("📈 Stock Price Chart")

df = pd.DataFrame({
    "Date": dates,
    "Close Price": prices
})

st.line_chart(df.set_index("Date"))

# -----------------------------
# PORTFOLIO
# -----------------------------
st.subheader("💼 Portfolio")

cur.execute("""
SELECT symbol, shares, buy_price, buy_date
FROM portfolio
ORDER BY buy_date;
""")

portfolio = cur.fetchall()

total_shares = 0
total_value = 0
total_profit = 0

if len(portfolio) == 0:
    st.info("No shares in portfolio.")
else:

    for symbol, shares, buy_price, buy_date in portfolio:

        shares = int(shares)
        buy_price = float(buy_price)

        current_price = latest
        current_value = current_price * shares
        invested = buy_price * shares
        profit = current_value - invested

        total_shares += shares
        total_value += current_value
        total_profit += profit

        st.markdown(f"### 📈 {symbol}")
        st.write(f"**Shares:** {shares}")
        st.write(f"**Buy Price:** ${buy_price:.2f}")
        st.write(f"**Current Price:** ${current_price:.2f}")
        st.write(f"**Current Value:** ${current_value:.2f}")
        st.write(f"**Buy Date:** {buy_date}")

        if profit >= 0:
            st.success(f"Profit: +${profit:.2f}")
        else:
            st.error(f"Loss: ${profit:.2f}")

        st.write("---")

    st.subheader("📊 Portfolio Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Shares", total_shares)

    with c2:
        st.metric("Portfolio Value", f"${total_value:.2f}")

    with c3:
        st.metric("Profit / Loss", f"${total_profit:.2f}")
# -----------------------------
# FINAL SUMMARY
# -----------------------------
st.divider()

st.subheader("📋 AI Trading Summary")

st.write(f"**Stock:** {stock_symbol}")
st.write(f"**Latest Price:** ${latest:.2f}")
st.write(f"**3-Day Moving Average:** ${moving_average:.2f}")
st.write(f"**Predicted Tomorrow Price:** ${prediction:.2f}")
st.write(f"**AI Decision:** {decision}")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption("🤖 AI Trading Manager")
st.caption("Built with Python • PostgreSQL • Streamlit • Machine Learning")

# -----------------------------
# CLOSE DATABASE
# -----------------------------
cur.close()
conn.close()        