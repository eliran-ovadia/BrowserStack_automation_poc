from time import sleep

import pytest

from src.flows.login_flow import LoginFlow
from src.page_factory import PageFactory


@pytest.mark.usefixtures("set_web_driver")
class TestTrading:

    @pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):
        pf = PageFactory(set_web_driver)


        login_flow = LoginFlow(set_web_driver).login_with_credentials()
        dashboard = pf.dashboard().nav_trade_portfolio()

        sleep(5)
