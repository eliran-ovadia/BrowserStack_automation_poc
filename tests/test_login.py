import pytest

from src.flows.login_flow import LoginFlow

@pytest.mark.usefixtures("set_web_driver")
class TestLogin:

    def xtest_reach_demo(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_demo()

    def xtest_reach_trade(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_trade()

    def xtest_enter_profile(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_profile()

    def xtest_enter_currency_exchange(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_currency_exchange()

    def test_moving_between_pages(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        portfolio = dashboard.enter_trade()
        market = portfolio.enter_market_page()
        search = market.enter_search_page()
        orders = search.enter_orders_page()
        knowledge = orders.enter_knowledge_page()
