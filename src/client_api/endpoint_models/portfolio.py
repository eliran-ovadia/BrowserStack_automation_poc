
class PortfolioEndpoint:
    def __init__(self, **kwargs):
        self._holdings: list[dict] = kwargs.get("holdings", [])


    def get_holdings_names(self):
        symbols = []
        for holding in self._holdings:

            symbols.append(holding.get("symbol"))
        return symbols

    def get_holdings(self):
        return self._holdings