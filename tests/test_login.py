from time import sleep

import pytest

from src.components.navbar import NavBar
from src.flows.login_flow import LoginFlow
from src.page_factory import PageFactory
from src.pages.dashboard_page import DashboardPage
from src.pages.portfolio_page import PortfolioPage
from src.pages.terms_page import TermsPage
from tests.conftest import set_web_driver


@pytest.mark.usefixtures("set_web_driver")
class TestLogin:

    @pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):
        # terms = TermsPage(set_web_driver)
        # terms.accept_terms()
        login_flow = LoginFlow(set_web_driver).login_with_credentials()
        dashboard = DashboardPage(set_web_driver).nav_trade_portfolio()
        portfolio = PortfolioPage(set_web_driver).enter_portfolio_analysis()
        sleep(10)