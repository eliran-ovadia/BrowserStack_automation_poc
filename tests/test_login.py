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

    def test_enter_currency_exchange(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_currency_exchange()

    def test_enter_invite_friend(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_invite_your_friend()

    def test_enter_fund_my_account(self, set_web_driver):
        dashboard = LoginFlow(set_web_driver).login_with_email_and_password()
        dashboard.enter_fund_my_account()