import psycopg2


class FeedbackAI:

    def __init__(self):

        print("=" * 60)
        print("🏆 FEEDBACK AI")
        print("=" * 60)

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        print("✅ Feedback AI Connected")

    # =====================================
    # SAVE TRADE RESULT
    # =====================================

    def save_feedback(
        self,
        symbol,
        decision,
        profit_loss,
        outcome
    ):

        if profit_loss > 0:
            outcome = "WIN"

        elif profit_loss < 0:
            outcome = "LOSS"

        else:
            outcome = "BREAKEVEN"

        self.cur.execute("""

            INSERT INTO trade_feedback(

                symbol,

                final_decision,

                profit_loss,

                outcome

            )

            VALUES(%s,%s,%s,%s)

        """, (

            symbol,

            decision,

            profit_loss,

            outcome

        ))

        self.conn.commit()

        print()
        print("🏆 Trade Feedback Saved")
        print("--------------------------")
        print("Symbol :", symbol)
        print("Decision :", decision)
        print("Profit :", profit_loss)
        print("Outcome :", outcome)

    # =====================================
    # SHOW FEEDBACK HISTORY
    # =====================================

    def show_feedback(self):

        self.cur.execute("""

            SELECT

                symbol,

                final_decision,

                profit_loss,

                outcome

            FROM trade_feedback

            ORDER BY id DESC

        """)

        rows = self.cur.fetchall()

        print()
        print("=" * 60)
        print("🏆 TRADE FEEDBACK")
        print("=" * 60)

        for row in rows:

            print(row)

    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        self.cur.close()

        self.conn.close()

        print("✅ Feedback AI Closed")


if __name__ == "__main__":

    ai = FeedbackAI()

    ai.save_feedback(

        "AAPL",

        "BUY",

        120

    )

    ai.show_feedback()

    ai.close()