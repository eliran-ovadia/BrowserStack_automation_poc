from src.pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
