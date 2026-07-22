class RiskAI:

    def __init__(self,
                 account_balance=10000,
                 max_risk_percent=2):

        self.account_balance = account_balance
        self.max_risk_percent = max_risk_percent

    def check_trade(self, shares, price):

        trade_value = shares * price

        max_allowed = (
            self.account_balance *
            self.max_risk_percent
        ) / 100

        if trade_value <= max_allowed:

            return {
                "approved": True,
                "message": "Trade Approved",
                "max_allowed": max_allowed
            }

        else:

            return {
                "approved": False,
                "message": "Trade Rejected",
                "max_allowed": max_allowed
            }