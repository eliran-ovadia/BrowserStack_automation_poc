from client_api.utils.api_auth import ApiAuth, handle_request
from endpoint_models.portfolio import PortfolioEndpoint


class ApiClient(ApiAuth):
    def __init__(self):
        super().__init__()

    def get_holdings_symbols(self):
        url = f"{self.base_url}/api/dual/account/portfolio?account=IBI1022"
        api_call = lambda: self.session.get(url)
        response = handle_request(api_call)
        model = PortfolioEndpoint(**response)
        return model.get_holdings_names()


if __name__ == "__main__":
    api_client = ApiClient()
    symbols = api_client.get_holdings_symbols()
    print(symbols)
