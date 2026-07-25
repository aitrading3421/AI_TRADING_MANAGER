import psycopg2
from datetime import datetime


class ErrorMonitorAI:

    def __init__(self):

        print("=" * 60)
        print("🚨 ERROR MONITOR AI")
        print("=" * 60)

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        print("✅ Error Monitor Connected")

    # ==========================================
    # SAVE ERROR
    # ==========================================

    def save_error(self, module, error):

        self.cur.execute("""

            INSERT INTO system_logs
            (module, level, message, log_time)

            VALUES
            (%s, %s, %s, %s)

        """, (

            module,
            "ERROR",
            str(error),
            datetime.now()

        ))

        self.conn.commit()

        print("🚨 Error Logged Successfully")

    # ==========================================
    # CLOSE
    # ==========================================

    def close(self):

        self.cur.close()
        self.conn.close()

        print("✅ Error Monitor Closed")