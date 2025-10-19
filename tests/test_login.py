import pytest

from src.flows.login_flow import LoginFlow
from src.page_factory import PageFactory


@pytest.mark.usefixtures("set_web_driver")
class TestLogin:

    def xtest_reach_demo(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_demo()

    def xtest_reach_trade(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.nav_trade()

    def xtest_enter_profile(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_profile()

    def xtest_enter_currency_exchange(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_currency_exchange()

    #@pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):
        pf = PageFactory(set_web_driver)
        dashboard = LoginFlow(set_web_driver, pf).login_with_email_and_password().nav_trade()
        portfolio = pf.portfolio()
        portfolio.navbar.tap_search()
        search = pf.search()
        search.navbar.tap_market()
