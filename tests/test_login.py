import pytest

from src.flows.login_flow import LoginFlow

@pytest.mark.usefixtures('setWebdriver') # Remove to run locally
class TestLogin:
    def test_login(self, setWebdriver):
        dashboard = LoginFlow(setWebdriver).login_with_email_and_password()