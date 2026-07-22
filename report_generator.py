import psycopg2

def generate_report():

    conn = psycopg2.connect(
        host="localhost",
        database="trading_ai",
        user="postgres",
        password="aitrading",
        port="5432"
    )

    cur = conn.cursor()

    # Account Balance
    cur.execute("SELECT balance FROM account LIMIT 1;")
    balance = float(cur.fetchone()[0])

    # Portfolio Summary
    cur.execute("SELECT shares, buy_price FROM portfolio;")
    rows = cur.fetchall()

    total_shares = 0
    invested = 0

    for shares, buy_price in rows:
        total_shares += shares
        invested += shares * float(buy_price)

    report = f"""
AI TRADING MANAGER REPORT

==============================

Account Balance : ${balance:.2f}

Total Shares : {total_shares}

Money Invested : ${invested:.2f}

Portfolio Positions : {len(rows)}

==============================

Generated Automatically
"""

    cur.close()
    conn.close()

    return report