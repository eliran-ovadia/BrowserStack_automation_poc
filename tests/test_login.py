from time import sleep

import pytest

from src.pages.dashboard_page import DashboardPage
from src.flows.login_flow import LoginFlow


@pytest.mark.usefixtures("set_web_driver")
class TestTrading:

    @pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):

        login_flow = LoginFlow(set_web_driver).login_with_credentials()
        dashboard = DashboardPage(set_web_driver).nav_trade_portfolio()

        sleep(5)
