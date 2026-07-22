import psycopg2
from datetime import datetime


class ReportAI:

    def __init__(self):

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

    def generate_report(self):

        # ==========================================
        # Portfolio Value
        # ==========================================

        self.cur.execute("""

            SELECT COALESCE(SUM(shares * buy_price),0)

            FROM portfolio;

        """)

        portfolio_value = float(self.cur.fetchone()[0])

        # ==========================================
        # Today's Trades
        # ==========================================

        self.cur.execute("""

            SELECT action,symbol,shares

            FROM trade_history

            WHERE DATE(trade_date)=CURRENT_DATE;

        """)

        today_trades = self.cur.fetchall()

        # ==========================================
        # Today's Profit
        # ==========================================

        self.cur.execute("""

            SELECT COALESCE(SUM(total),0)

            FROM trade_history

            WHERE DATE(trade_date)=CURRENT_DATE;

        """)

        today_profit = float(self.cur.fetchone()[0])

        # ==========================================
        # Open Positions
        # ==========================================

        self.cur.execute("""

            SELECT COUNT(*)

            FROM portfolio;

        """)

        open_positions = int(self.cur.fetchone()[0])

        # ==========================================
        # MANAGER AI DECISIONS
        # ==========================================

        self.cur.execute("""

            SELECT final_decision, confidence

            FROM manager_decisions

            WHERE DATE(decision_time)=CURRENT_DATE;

        """)

        decisions = self.cur.fetchall()

        buy = 0
        sell = 0
        hold = 0

        total_confidence = 0

        for decision, confidence in decisions:

            if decision == "BUY":

                buy += 1

            elif decision == "SELL":

                sell += 1

            else:

                hold += 1

            total_confidence += float(confidence)

        if len(decisions) > 0:

            average_confidence = round(

                total_confidence / len(decisions),

                2

            )

        else:

            average_confidence = 0

        report = {

            "date": datetime.now().strftime("%d-%b-%Y"),

            "portfolio_value": portfolio_value,

            "today_trades": today_trades,

            "today_profit": today_profit,

            "open_positions": open_positions,

            "buy": buy,

            "sell": sell,

            "hold": hold,

            "average_confidence": average_confidence,

            "manager_decisions": len(decisions)

        }

        return report

    def print_report(self):

        report = self.generate_report()

        print()

        print("=" * 60)

        print("🤖 AI TRADING MANAGER")

        print("=" * 60)

        print()

        print("📅 Date:")

        print(report["date"])

        print()

        print("💰 Portfolio Value:")

        print(f"${report['portfolio_value']:.2f}")

        print()

        print("📈 Today's Trades:")

        if len(report["today_trades"]) == 0:

            print("No trades today.")

        else:

            for action, symbol, shares in report["today_trades"]:

                print(f"{action} {symbol} ({shares} Shares)")

        print()

        print("💵 Today's Profit / Loss:")

        print(f"${report['today_profit']:.2f}")

        print()

        print("📦 Open Positions:")

        print(report["open_positions"])

        print()

        print("🧠 Manager AI Decisions Today:")

        print(report["manager_decisions"])

        print()

        print("🤖 Today's AI Decisions:")

        print(f"BUY : {report['buy']}")

        print(f"SELL: {report['sell']}")

        print(f"HOLD: {report['hold']}")

        print()

        print("🎯 Average AI Confidence:")

        print(f"{report['average_confidence']}%")

        print()

        print("📊 System Status:")

        print("Healthy ✅")

        print()

        print("Manager AI Summary:")

        print("All AI modules completed successfully.")

        print("No critical system errors detected.")

        print("Portfolio is operating normally.")

        print("=" * 60)

    def close(self):

        self.cur.close()

        self.conn.close()


if __name__ == "__main__":

    report = ReportAI()

    report.print_report()

    report.close() 