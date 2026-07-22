import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD


class MarketAI:

    def __init__(self, symbol="AAPL"):

        self.symbol = symbol

    def analyze_market(self):

        # ==========================================
        # DOWNLOAD MARKET DATA
        # ==========================================

        stock = yf.Ticker(self.symbol)

        data = stock.history(period="3mo")

        if data.empty:

            raise Exception("No market data downloaded.")

        prices = data["Close"]

        latest_price = float(prices.iloc[-1])

        moving_average = float(prices.tail(20).mean())

        # ==========================================
        # RSI
        # ==========================================

        rsi = RSIIndicator(

            close=prices,

            window=14

        )

        rsi_value = float(

            rsi.rsi().iloc[-1]

        )

        # ==========================================
        # MACD
        # ==========================================

        macd = MACD(

            close=prices

        )

        macd_value = float(

            macd.macd().iloc[-1]

        )

        signal_value = float(

            macd.macd_signal().iloc[-1]

        )

        # ==========================================
        # AI SCORING VARIABLES
        # ==========================================

        score = 0

        confidence = 0

        reasons = []


        # ==========================================
        # RSI WEIGHT
        # ==========================================

        if rsi_value < 30:

            score += 35

            reasons.append("RSI Oversold (+35)")

        elif rsi_value > 70:

            score -= 35

            reasons.append("RSI Overbought (-35)")

        else:

            reasons.append("RSI Neutral")

        # ==========================================
        # MACD WEIGHT
        # ==========================================

        if macd_value > signal_value:

            score += 40

            reasons.append("MACD Bullish (+40)")

        elif macd_value < signal_value:

            score -= 40

            reasons.append("MACD Bearish (-40)")

        else:

            reasons.append("MACD Neutral")

        # ==========================================
        # MOVING AVERAGE WEIGHT
        # ==========================================

        if latest_price > moving_average:

            score += 25

            reasons.append("Price Above MA (+25)")

        elif latest_price < moving_average:

            score -= 25

            reasons.append("Price Below MA (-25)")

        else:

            reasons.append("Price At MA")         

        # ==========================================
        # FINAL DECISION
        # ==========================================

        if score >= 80:

            decision = "STRONG BUY"

        elif score >= 40:

            decision = "BUY"

        elif score <= -80:

            decision = "STRONG SELL"

        elif score <= -40:

            decision = "SELL"

        else:

            decision = "HOLD"

        # ==========================================
        # CONFIDENCE
        # ==========================================

        confidence = abs(score)

        if confidence > 100:

            confidence = 100

        confidence = round(confidence, 2)

        # ==========================================
        # REASON
        # ==========================================

        if len(reasons) == 0:

            reason = "No strong market signals"

        else:

            reason = " | ".join(reasons)

        print()

        print("=" * 60)

        print("📈 MARKET AI ANALYSIS")

        print("=" * 60)

        print(f"Latest Price   : {latest_price:.2f}")

        print(f"Moving Average : {moving_average:.2f}")

        print(f"RSI            : {rsi_value:.2f}")

        print(f"MACD           : {macd_value:.4f}")

        print(f"Signal         : {signal_value:.4f}")

        print("--------------------------------------------")

        print(f"Market Score   : {score}")

        print(f"Decision       : {decision}")

        print(f"Confidence     : {confidence}%")

        print(f"Reason         : {reason}")

        print("=" * 60)         

        # ==========================================
        # RETURN RESULTS
        # ==========================================

        return {

            "symbol": self.symbol,

            "latest_price": latest_price,

            "moving_average": round(moving_average, 2),

            "rsi": round(rsi_value, 2),

            "macd": round(macd_value, 4),

            "signal": round(signal_value, 4),

            "score": score,

            "decision": decision,

            "confidence": confidence,

            "reason": reason

        }


# ==========================================
# TEST MARKET AI
# ==========================================

if __name__ == "__main__":

    market_ai = MarketAI()

    result = market_ai.analyze_market()

    print()

    print("=" * 60)

    print("📊 MARKET AI V3 SUMMARY")

    print("=" * 60)

    print(f"Symbol         : {result['symbol']}")

    print(f"Latest Price   : {result['latest_price']:.2f}")

    print(f"Decision       : {result['decision']}")

    print(f"Confidence     : {result['confidence']}%")

    print(f"Score          : {result['score']}")

    print(f"Reason         : {result['reason']}")

    print("=" * 60)      