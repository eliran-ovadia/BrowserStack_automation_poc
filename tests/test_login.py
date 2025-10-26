import pytest

from src.flows.login_flow import LoginFlow
from src.page_factory import PageFactory


@pytest.mark.usefixtures("set_web_driver")
class TestLogin:

    @pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):
        pf = PageFactory(set_web_driver)
        portfolio = LoginFlow(set_web_driver, pf).enter_trade_with_credentials().enter_portfolio_analysis()