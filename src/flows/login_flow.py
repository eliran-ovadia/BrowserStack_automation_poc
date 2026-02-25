from src.flows.base_flow import BaseFlow

from src.pages.welcome_page import WelcomePage
from src.pages.dashboard_page import DashboardPage
from src.pages.login_with_password_page import LoginWithPasswordPage
from src.pages.otp_page import OtpPage
from src.pages.portfolio_page import PortfolioPage
from src.pages.terms_page import TermsPage


class LoginFlow(BaseFlow):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.platform = (driver.capabilities.get("platformName") or "").lower()

    def login_with_credentials(self):
        if self.platform == "android":
            terms = TermsPage(self.driver)
            terms.accept_terms()

        welcome = WelcomePage(self.driver)
        welcome.enter_username()
        welcome.tap_welcome_login()

        otp = OtpPage(self.driver)
        otp.tap_login_with_password()

        password_login = LoginWithPasswordPage(self.driver)
        password_login.enter_password()
        password_login.tap_password_login()

        dashboard = DashboardPage(self.driver)
        return dashboard

    def enter_trade_with_credentials(self):
        dashboard = self.login_with_credentials()
        dashboard.nav_trade_portfolio()

        portfolio = PortfolioPage(self.driver)
        return portfolio


