import psycopg2


class FusionAI:

    def __init__(self):

        print("=" * 60)
        print("🧠 AI FUSION ENGINE")
        print("=" * 60)

        # -----------------------------
        # DATABASE CONNECTION
        # -----------------------------

        self.conn = psycopg2.connect(
            host="localhost",
            database="trading_ai",
            user="postgres",
            password="aitrading",
            port="5432"
        )

        self.cur = self.conn.cursor()

        self.cur.execute("SELECT current_database();")
        print("DATABASE =", self.cur.fetchone()[0])

        print("✅ Connected to PostgreSQL")

    # ==========================================
    # MARKET SCORE
    # ==========================================

    def market_score(self, decision):

        if decision == "BUY":
            return 40

        elif decision == "SELL":
            return -40

        return 0

    # ==========================================
    # NEWS SCORE
    # ==========================================

    def news_score(self, sentiment):

        if sentiment == "POSITIVE":
            return 35

        elif sentiment == "NEGATIVE":
            return -35

        return 0

    # ==========================================
    # RISK SCORE
    # ==========================================

    def risk_score(self, risk_level):

        risk_level = risk_level.upper()

        if risk_level == "LOW":
            return 25

        elif risk_level == "MEDIUM":
            return 10

        elif risk_level == "HIGH":
            return -40

        return 0

    # ==========================================
    # FUSION ENGINE
    # ==========================================

    def fusion_decision(

        self,

        market_decision,

        news_sentiment,

        risk_level

    ):

        # -----------------------------
        # GET SCORES
        # -----------------------------

        market = self.market_score(market_decision)

        news = self.news_score(news_sentiment)

        risk = self.risk_score(risk_level)

        total_score = market + news + risk

        # -----------------------------
        # FINAL DECISION
        # -----------------------------

        if total_score >= 50:

            final_decision = "BUY"

        elif total_score <= -50:

            final_decision = "SELL"

        else:

            final_decision = "HOLD"

        # -----------------------------
        # BUILD REASON
        # -----------------------------

        reasons = []

        reasons.append(f"Market={market_decision}")

        reasons.append(f"News={news_sentiment}")

        reasons.append(f"Risk={risk_level}")

        reason = " | ".join(reasons)

        print()

        print("=" * 60)

        print("🧠 AI FUSION RESULT")

        print("=" * 60)

        print(f"Market Score : {market}")

        print(f"News Score   : {news}")

        print(f"Risk Score   : {risk}")

        print("------------------------------")

        print(f"Total Score  : {total_score}")

        print()

        print(f"Decision     : {final_decision}")

        print(f"Reason       : {reason}")

        print("=" * 60)

        return {

            "market_score": market,

            "news_score": news,

            "risk_score": risk,

            "total_score": total_score,

            "decision": final_decision,

            "reason": reason

        }        


    # ==========================================
    # CONFIDENCE CALCULATOR
    # ==========================================

    def calculate_confidence(self, total_score):

        # Maximum absolute score
        max_score = 100

        confidence = (abs(total_score) / max_score) * 100

        if confidence > 100:
            confidence = 100

        confidence = round(confidence, 2)

        return confidence


    # ==========================================
    # FUSION SUMMARY
    # ==========================================
 
    def fusion_summary(

        self,

        market_decision,

        market_confidence,

        news_sentiment,

        news_confidence,

        risk_level,

         risk_confidence
   
    ):
        result = self.fusion_decision(

            market_decision,

            news_sentiment,

            risk_level

        )

        confidence = self.calculate_confidence(

            result["total_score"]

        )

        print()
        print("=" * 60)
        print("🤖 AI FUSION SUMMARY")
        print("=" * 60)

        print(f"Market Decision : {market_decision}")
        print(f"News Sentiment  : {news_sentiment}")
        print(f"Risk Level      : {risk_level}")

        print("--------------------------------------------")

        print(f"Final Decision  : {result['decision']}")
        print(f"Confidence      : {confidence}%")

        print(f"Reason          : {result['reason']}")

        print("=" * 60)

        result["confidence"] = confidence

        return result

    # ==========================================
    # SAVE DECISION
    # ==========================================

    def save_decision(

    self,

    symbol,

    market_decision,

    market_confidence,

    news_sentiment,

    news_confidence,

    risk_level,

    risk_confidence

    ):

        result = self.fusion_summary(

           market_decision,

           market_confidence,

           news_sentiment,

           news_confidence,

           risk_level,

           risk_confidence

    )

        self.cur.execute("""

            INSERT INTO manager_decisions(

                symbol,

                market_decision,
                market_confidence,

                news_sentiment,
                news_confidence,

                risk_level,
                risk_confidence,

                final_decision,
                confidence,
                reason

            )

             VALUES(
                  %s,%s,%s,
                  %s,%s,
                  %s,%s,
                  %s,%s,%s
            )

        """,  (
                 symbol,
                 market_decision,
                 market_confidence,
                 news_sentiment,
                 news_confidence,
                 risk_level,
                 risk_confidence,
                 result["decision"],
                 result["confidence"],
                 result["reason"]

        ))

        self.conn.commit()

        print()
        print("💾 Fusion decision saved successfully.")

        return result


    # ==========================================
    # CLOSE
    # ==========================================

    def close(self):

        self.cur.close()

        self.conn.close()

        print("✅ Fusion AI Closed")


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    fusion = FusionAI()

    fusion.save_decision(

        symbol="AAPL",

        market_decision="BUY",

        news_sentiment="POSITIVE",

        risk_level="LOW"

    )

    fusion.close()        