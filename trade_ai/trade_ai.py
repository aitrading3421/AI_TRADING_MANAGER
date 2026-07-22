import psycopg2
from datetime import datetime


class TradeAI:

    def __init__(self):

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

    def execute_trade(self, symbol, decision, shares, price):

        total = shares * price

        if decision == "BUY":

            self.cur.execute("""
                INSERT INTO portfolio
                (symbol, shares, buy_price, buy_date)
                VALUES (%s,%s,%s,%s)
            """,
            (
                symbol,
                shares,
                price,
                datetime.now()
            ))

        self.cur.execute("""
            INSERT INTO trade_history
            (symbol, action, shares, price, total)
            VALUES (%s,%s,%s,%s,%s)
        """,
        (
            symbol,
            decision,
            shares,
            price,
            total
        ))

        self.conn.commit()

        return {
            "status": "SUCCESS",
            "decision": decision,
            "shares": shares,
            "price": price,
            "total": total
        }

    def close(self):
        self.cur.close()
        self.conn.close()