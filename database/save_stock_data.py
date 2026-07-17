import psycopg2
import yfinance as yf

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

# Download 3 months of Apple stock data
stock = yf.Ticker("AAPL")
data = stock.history(period="3mo")

# Save data into PostgreSQL
for index, row in data.iterrows():
    cur.execute("""
        INSERT INTO stock_prices
        (symbol, trade_date, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, trade_date) DO NOTHING;
    """, (
        "AAPL",
        index.date(),
        float(row["Open"]),
        float(row["High"]),
        float(row["Low"]),
        float(row["Close"]),
        int(row["Volume"])
    ))

conn.commit()

print("✅ Stock data saved successfully!")

cur.close()
conn.close()