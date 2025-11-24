from asyncio import sleep

import pytest

from src.components.navbar import NavBar
from src.flows.login_flow import LoginFlow
from src.page_factory import PageFactory
from tests.conftest import set_web_driver


@pytest.mark.usefixtures("set_web_driver")
class TestLogin:

    @pytest.mark.smoke
    def test_moving_between_pages(self, set_web_driver):
        sleep(20)

