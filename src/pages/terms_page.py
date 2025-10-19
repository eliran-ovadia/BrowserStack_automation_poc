from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class TermsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators ----------------------
        self.accept_button = {
            "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Accept"]'),
            "ios": ("", "")
        }
        self.reject_button = {
            "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Reject"]'),
            "ios": ("", "")
        }

    def accept_terms(self):
        self.tap(self.accept_button)

    def reject_terms(self):
        self.tap(self.reject_button)
