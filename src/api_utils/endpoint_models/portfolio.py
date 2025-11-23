

class PortfolioEndpoint:
    def __init__(self, **kwargs):
        self._holdings = kwargs.get("holdings")

    def get_holdings(self):
        return self._holdings