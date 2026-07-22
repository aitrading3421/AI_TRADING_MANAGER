from memory_ai.memory_ai import MemoryAI
from fusion_ai.fusion_ai import FusionAI
from market_ai.market_ai import MarketAI
from news_ai.news_ai import NewsAI
from rule_engine.rule_engine import RuleEngine
from risk_ai.risk_ai import RiskAI
from trade_ai.trade_ai import TradeAI
from report_ai.report_ai import ReportAI

import psycopg2


class ManagerAI:

    def __init__(self):

        print("=" * 60)
        print("🤖 AI TRADING MANAGER V2")
        print("=" * 60)

        # -----------------------------
        # DATABASE
        # -----------------------------

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        # -----------------------------
        # LOAD ALL AI MODULES
        # -----------------------------

        print("Loading AI Modules...\n")

        self.market_ai = MarketAI()

        self.news_ai = NewsAI()

        self.rule_engine = RuleEngine()

        self.risk_ai = RiskAI(
            account_balance=10000,
            max_risk_percent=2
        )

        self.trade_ai = TradeAI()

        self.report_ai = ReportAI()

        self.fusion_ai = FusionAI()

        self.memory_ai = MemoryAI()

        print("✅ Market AI Loaded")
        print("✅ News AI Loaded")
        print("✅ Rule Engine Loaded")
        print("✅ Risk AI Loaded")
        print("✅ Trade AI Loaded")
        print("✅ Report AI Loaded")
        print("✅ Fusion AI Loaded")
        print("✅ Memory AI Loaded")

        print("\n✅ Manager AI Ready\n")

      # ==========================================
      # RUN MANAGER AI
      # ==========================================

    def run(self):

        print("=" * 60)
        print("🚀 MANAGER AI STARTED")
        print("=" * 60)

        # ---------------------------------
        # MARKET AI
        # ---------------------------------

        print("\n📈 Running Market AI...\n")

        market = self.market_ai.analyze_market()

        print("✅ Market AI Finished")

        # ---------------------------------
        # NEWS AI
        # ---------------------------------

        print("\n📰 Running News AI...\n")

        articles = self.news_ai.fetch_news()

        self.news_ai.analyze_news(articles)

        print("✅ News AI Finished")

        # ---------------------------------
        # GET LATEST NEWS SENTIMENT
        # ---------------------------------

        self.cur.execute("""

            SELECT sentiment

            FROM news_cache

            ORDER BY id DESC

            LIMIT 1

        """)

        row = self.cur.fetchone()

        if row:

            news_sentiment = row[0]

        else:

            news_sentiment = "UNKNOWN"

        print()
        print("Latest News Sentiment :", news_sentiment)

        # ---------------------------------
        # RULE ENGINE
        # ---------------------------------

        decision =self.rule_engine.evaluate(market)

        print()
        print("Market Decision :",
        market["decision"])
        print("Market Confidence :",
        market["confidence"], "%")

       
        # ---------------------------------
        # FUSION AI
        # ---------------------------------

        print("\n🧠 Running Fusion AI...\n")

        # For now we'll assume LOW risk.
        # Later we'll replace this with the actual Risk AI output.
        risk_level = "LOW"

        fusion_result = self.fusion_ai.save_decision(

             symbol=market["symbol"],

             market_decision=market["decision"],

             market_confidence=market["confidence"],

             news_sentiment=news_sentiment,

             news_confidence=90,

             risk_level=risk_level,

             risk_confidence=95

        )
        manager_decision = fusion_result["decision"]

        print()

        print("👑 Final Manager Decision :", manager_decision)

        print("🔥 Confidence :", fusion_result["confidence"], "%")

        print("📝 Reason :", fusion_result["reason"])

        # ---------------------------------
        # RISK AI
        # ---------------------------------

        print("\n🛡 Running Risk AI...\n")

        risk = self.risk_ai.check_trade(
            shares=1,
            price=market["latest_price"]
        )

        if risk["approved"]:

            print("✅ Risk AI Approved")

            if manager_decision != "HOLD":

                print("\n💹 Executing Trade...\n")

                self.trade_ai.execute_trade(
                    market["symbol"],
                    manager_decision,
                    1,
                    market["latest_price"]
                )

                print("✅ Trade Executed")

                manager_status = "TRADE_EXECUTED"

            else:

                print("⏸ Manager AI decided HOLD")

                manager_status = "HOLD"

        else:

            print("❌ Trade Blocked By Risk AI")

            manager_status = "BLOCKED_BY_RISK"

        # ---------------------------------
        # SAVE MANAGER EVENT
        # ---------------------------------

        self.cur.execute("""

            INSERT INTO manager_events
            (event, status)

            VALUES
            (%s,%s)

        """, (

            f"Decision : {manager_decision}",

            manager_status

        ))

        self.conn.commit()

        print("✅ Manager Event Saved")

        # ---------------------------------
        # REPORT AI
        # ---------------------------------

        print("\n📄 Generating Report...\n")

        self.report_ai.print_report()

        print("\n✅ Report Generated")  

        # ==========================================
        # CLOSE
        # ==========================================

    def close(self):

        print("\nClosing AI Modules...")

        try:
            self.news_ai.close()
        except:
            pass

        try:
            self.trade_ai.close()
        except:
            pass

        try:
            self.report_ai.close()
        except:
            pass

        try:
            self.fusion_ai.close()
        except:
            pass    

        self.cur.close()
        self.conn.close()

        print("✅ Manager AI Closed")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    manager = ManagerAI()

    try:

        manager.run()

        print()
        print("=" * 60)
        print("🎉 AI TRADING MANAGER COMPLETED")
        print("=" * 60)

    except Exception as e:

        print()
        print("=" * 60)
        print("❌ MANAGER AI ERROR")
        print("=" * 60)
        print(e)

    finally:

        manager.close()     