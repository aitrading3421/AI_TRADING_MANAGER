import psycopg2
from datetime import date

# AI Decision (Later this will come from predictor.py)
decision = "BUY"

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
price = 330.57

if decision == "BUY":
    cur.execute("""
    INSERT INTO portfolio (symbol, shares, buy_price, buy_date)
    VALUES (%s, %s, %s, %s)
    """, (symbol, shares, price, date.today()))

    conn.commit()
    print("✅ AI bought 10 shares of AAPL")

elif decision == "SELL":
    cur.execute("""
    DELETE FROM portfolio
    WHERE id = (
        SELECT id
        FROM portfolio
        WHERE symbol=%s
        ORDER BY id
        LIMIT 1
    )
    """, (symbol,))

    conn.commit()
    print("🔴 AI sold shares")

else:
    print("🟡 AI decided to HOLD")

cur.close()
conn.close()