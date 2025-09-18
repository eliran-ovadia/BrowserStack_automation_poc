# flows/login_flow.py

from src.flows.base_flow import BaseFlow
from src.pages.terms_page import TermsPage


class LoginFlow(BaseFlow):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def login_with_email_and_password(self):
        self.log_step("Logging in with email and password")

        dashboard = (
            TermsPage(self.driver)
            .accept_terms()
            .enter_username()
            .tap_welcome_login()
            .tap_login_with_password()
            .enter_password()
            .tap_password_login()
        )
        self.log_step("Reached Dashboard")
        return dashboard
