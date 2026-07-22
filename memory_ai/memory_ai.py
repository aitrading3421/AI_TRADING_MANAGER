import psycopg2


class MemoryAI:

    def __init__(self):

        print("=" * 60)
        print("🧠 MEMORY AI")
        print("=" * 60)

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        print("✅ Memory AI Connected")

    # ==========================================
    # SAVE MEMORY
    # ==========================================

    def save_memory(

        self,

        symbol,

        market_decision,
        market_confidence,

        news_sentiment,
        news_confidence,

        risk_level,
        risk_confidence,

        final_decision,
        final_confidence

    ):

        self.cur.execute("""

        INSERT INTO memory_history(

            symbol,

            market_decision,
            market_confidence,

            news_sentiment,
            news_confidence,

            risk_level,
            risk_confidence,

            final_decision,
            final_confidence

        )

        VALUES(

            %s,%s,%s,
            %s,%s,
            %s,%s,
            %s,%s

        )

        """, (

            symbol,

            market_decision,
            market_confidence,

            news_sentiment,
            news_confidence,

            risk_level,
            risk_confidence,

            final_decision,
            final_confidence

        ))

        self.conn.commit()

        print("🧠 Memory Saved Successfully")

    # ==========================================
    # CLOSE
    # ==========================================

    def close(self):

        self.cur.close()
        self.conn.close()

        print("✅ Memory AI Closed")


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    memory = MemoryAI()

    memory.save_memory(

        symbol="AAPL",

        market_decision="BUY",
        market_confidence=65,

        news_sentiment="POSITIVE",
        news_confidence=90,

        risk_level="LOW",
        risk_confidence=95,

        final_decision="BUY",
        final_confidence=100

    )

    memory.close()