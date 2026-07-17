import psycopg2
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
SELECT trade_date, close_price
FROM stock_prices
ORDER BY trade_date;
""")

rows = cur.fetchall()

print("Stock Closing Prices:\n")

prices = []

for row in rows:
    print(row)
    prices.append(row[1])

price_series = pd.Series(prices)

rsi = RSIIndicator(close=price_series, window=3)
rsi_value = rsi.rsi().iloc[-1]

print("\nRSI:", round(rsi_value, 2))
macd = MACD(close=price_series)
macd_value = macd.macd().iloc[-1]
signal_value = macd.macd_signal().iloc[-1]

print("MACD:", round(macd_value, 2))
print("Signal:", round(signal_value, 2))

moving_average = sum(prices[-3:]) / 3
latest = prices[-1]

print("3-Day Moving Average:", round(moving_average, 2))
print("Latest Price:", round(latest, 2))

if latest > moving_average and rsi_value < 70 and macd_value > signal_value:
    print("🟢 AI Decision: STRONG BUY")
elif latest < moving_average and rsi_value > 30 and macd_value < signal_value:
    print("🔴 AI Decision: STRONG SELL")
else:
    print("🟡 AI Decision: HOLD")

cur.close()
conn.close()