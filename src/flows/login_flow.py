from src.flows.base_flow import BaseFlow
from src.page_factory import PageFactory
from src.pages.terms_page import TermsPage


class LoginFlow(BaseFlow):

    def __init__(self, driver, factory: PageFactory | None = None):
        super().__init__(driver)
        self.driver = driver
        self.pf = factory or PageFactory(driver)
        self.page = TermsPage(driver)

    # ---------- Step-by-step (fluent internal API) ----------
    def accept_terms(self):
        self.log_step("Accepting terms and conditions")
        self.page.accept_terms()
        self.page = self.pf.welcome()
        return self

    def enter_username(self):
        self.page.enter_username()
        return self

    def tap_welcome_login(self):
        self.log_step("Tapping login on Welcome page")
        self.page.tap_welcome_login()
        self.page = self.pf.otp()
        return self

    def switch_to_password_page(self):
        self.log_step("Switching to password page")
        self.page.tap_login_with_password()
        self.page = self.pf.login_with_password()
        return self

    def enter_password(self):
        self.log_step("Entering password")
        self.page.enter_password()
        return self

    def tap_password_login(self):
        self.log_step("Tapping Login button with password")
        self.page.tap_password_login()
        self.page = self.pf.dashboard()
        return self

    def end(self):
        """Return the final page object after the flow completes."""
        self.log_step("Reached Dashboard")
        return self.page

    # ---------- Public API for tests ----------
    def login_with_email_and_password(self):
        return (
            self.accept_terms()
                .enter_username()
                .tap_welcome_login()
                .switch_to_password_page()
                .enter_password()
                .tap_password_login()
                .end()
        )
