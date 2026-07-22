import psycopg2


class LearningAI:

    def __init__(self):

        print("=" * 60)
        print("🧠 LEARNING AI")
        print("=" * 60)

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        print("✅ Learning AI Connected")

    # ==========================================
    # LOAD MEMORIES
    # ==========================================

    def load_memories(self):

        self.cur.execute("""

            SELECT

                symbol,
                market_decision,
                news_sentiment,
                risk_level,
                final_decision,
                final_confidence,
                outcome,
                profit_loss

            FROM memory_history

            ORDER BY memory_time DESC;

        """)

        memories = self.cur.fetchall()

        print()
        print("=" * 60)
        print("🧠 MEMORY HISTORY")
        print("=" * 60)

        if len(memories) == 0:
            print("No memories found.")
            return

        print("Total Memories :", len(memories))
        print("-" * 60)

        for row in memories:

            symbol = row[0]
            market = row[1]
            news = row[2]
            risk = row[3]
            decision = row[4]
            confidence = row[5]
            outcome = row[6]
            profit = row[7]

            print(f"""
📌 Symbol            : {symbol}
📈 Market Decision   : {market}
📰 News Sentiment    : {news}
🛡 Risk Level        : {risk}
🤖 Final Decision    : {decision}
🎯 Confidence        : {confidence}%
🏆 Outcome           : {outcome}
💰 Profit/Loss       : {profit}
------------------------------------------------------------
""")

    # ==========================================
    # SIMPLE LEARNING
    # ==========================================

    def learn(self):

        self.cur.execute("""

            SELECT
                outcome,
                final_confidence

            FROM memory_history

        """)

        rows = self.cur.fetchall()

        wins = 0
        losses = 0
        total_confidence = 0

        for outcome, confidence in rows:

            if outcome is not None:

                if outcome.upper() == "WIN":
                    wins += 1

                elif outcome.upper() == "LOSS":
                    losses += 1

            if confidence is not None:
                total_confidence += confidence

        total = wins + losses

        print()
        print("=" * 60)
        print("🧠 LEARNING SUMMARY")
        print("=" * 60)

        print("Total Trades :", total)
        print("Wins         :", wins)
        print("Losses       :", losses)

        if total > 0:

            win_rate = (wins / total) * 100
            avg_conf = total_confidence / len(rows)

            print(f"Win Rate     : {win_rate:.2f}%")
            print(f"Avg Confidence : {avg_conf:.2f}%")

        else:
            print("No completed trades yet.")

    # ==========================================
    # CLOSE
    # ==========================================

    def close(self):

        self.cur.close()
        self.conn.close()

        print()
        print("✅ Learning AI Closed")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    ai = LearningAI()

    ai.load_memories()

    ai.learn()

    ai.close() 