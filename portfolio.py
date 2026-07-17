import psycopg2
from datetime import date

conn = psycopg2.connect(
    host="localhost",
    database="trading_ai",
    user="postgres",
    password="aitrading",
    port="5432"
)

cur = conn.cursor()

symbol = "AAPL"
shares = 10
buy_price = 330.57

cur.execute("""
INSERT INTO portfolio (symbol, shares, buy_price, buy_date)
VALUES (%s, %s, %s, %s)
""", (symbol, shares, buy_price, date.today()))

conn.commit()

print("✅ Portfolio updated!")
print(f"Bought {shares} shares of {symbol} at ${buy_price}")

cur.close()
conn.close()