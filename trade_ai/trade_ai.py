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

    # ==========================================
    # BUY TRADE
    # ==========================================

    def execute_trade(self, symbol, decision, shares, price):

        total = shares * price

        profit_loss = 0

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

        elif decision == "SELL":

            # Find oldest BUY
            self.cur.execute("""
            SELECT id, shares, buy_price
            FROM portfolio
            WHERE symbol=%s
            ORDER BY buy_date ASC
            LIMIT 1
        """, (symbol,))

            row = self.cur.fetchone()

            if row:

                portfolio_id, owned_shares, buy_price = row

                profit_loss = (price - buy_price) * shares

                remaining = owned_shares - shares

            if remaining <= 0:

                self.cur.execute("""
                    DELETE FROM portfolio
                    WHERE id=%s
                """, (portfolio_id,))

            else:

                self.cur.execute("""
                    UPDATE portfolio
                    SET shares=%s
                    WHERE id=%s
                """,
                (
                    remaining,
                    portfolio_id
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
                "total": total,
                "profit_loss": profit_loss
            }

    # ==========================================
    # CLOSE TRADE (SELL)
    # ==========================================

    def close_trade(self, symbol, sell_price):

        # Find oldest open position
        self.cur.execute("""
            SELECT id, shares, buy_price
            FROM portfolio
            WHERE symbol=%s
            ORDER BY buy_date ASC
            LIMIT 1
        """, (symbol,))

        trade = self.cur.fetchone()

        if trade is None:

            print("❌ No open position found.")

            return None

        portfolio_id, shares, buy_price = trade

        # Calculate profit/loss
        profit_loss = (sell_price - buy_price) * shares

        # Save SELL trade
        self.cur.execute("""
            INSERT INTO trade_history
            (symbol, action, shares, price, total)
            VALUES (%s,%s,%s,%s,%s)
        """,
        (
            symbol,
            "SELL",
            shares,
            sell_price,
            shares * sell_price
        ))

        # Remove from portfolio
        self.cur.execute("""
            DELETE FROM portfolio
            WHERE id=%s
        """, (portfolio_id,))

        self.conn.commit()

        print()
        print("=" * 60)
        print("💰 TRADE CLOSED")
        print("=" * 60)
        print("Symbol      :", symbol)
        print("Buy Price   :", buy_price)
        print("Sell Price  :", sell_price)
        print("Shares      :", shares)
        print("Profit/Loss :", profit_loss)
        print("=" * 60)

        return {
            "symbol": symbol,
            "shares": shares,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "profit_loss": profit_loss
        }

    # ==========================================
    # CLOSE CONNECTION
    # ==========================================

    def close(self):

        self.cur.close()
        self.conn.close()

        print("✅ Trade AI Closed")


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    ai = TradeAI()

    # BUY Example
    ai.execute_trade(
        "AAPL",
        "BUY",
        5,
        300
    )

    # SELL Example
    ai.close_trade(
        "AAPL",
        325
    )

    ai.close() 