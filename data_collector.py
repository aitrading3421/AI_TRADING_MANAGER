import psycopg2
import yfinance as yf

conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

stock = yf.Ticker("AAPL")
data = stock.history(period="3mo")

for index, row in data.iterrows():
    print(index.date(), row["Close"])

cur.close()
conn.close()