from src.flows.base_flow import BaseFlow
from src.page_factory import PageFactory

class LoginFlow(BaseFlow):

    def __init__(self, driver, factory: PageFactory | None = None):
        super().__init__(driver)
        self.driver = driver
        self.platform = (driver.capabilities.get("platformName") or "").lower()
        self.pf = factory or PageFactory(driver)

    def login_with_credentials(self):
        if self.platform == "android":
            terms = self.pf.terms()
            terms.accept_terms()

        welcome = self.pf.welcome()
        welcome.enter_username()
        welcome.tap_welcome_login()

        otp = self.pf.otp()
        otp.tap_login_with_password()

        password_login = self.pf.login_with_password()
        password_login.enter_password()
        password_login.tap_password_login()

        dashboard = self.pf.dashboard()
        return dashboard

    def enter_trade_with_credentials(self):
        dashboard = self.login_with_credentials()
        dashboard.nav_trade_portfolio()

        portfolio = self.pf.portfolio()
        return portfolio


