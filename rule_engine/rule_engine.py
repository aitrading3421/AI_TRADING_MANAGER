class RuleEngine:

    def __init__(self):
        pass

    def evaluate(self, market_data):

        latest = market_data["latest_price"]
        average = market_data["moving_average"]
        rsi = market_data["rsi"]
        macd = market_data["macd"]
        signal = market_data["signal"]

        # BUY Rule
        if latest > average and rsi < 70 and macd > signal:
            return {
                "decision": "BUY",
                "confidence": 90
            }

        # SELL Rule
        elif latest < average and rsi > 30 and macd < signal:
            return {
                "decision": "SELL",
                "confidence": 90
            }

        # HOLD Rule
        else:
            return {
                "decision": "HOLD",
                "confidence": 75
            }