# pages/terms_page.py
from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.welcome_page import WelcomePage


class TermsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators ----------------------
        self.accept_button = {
            "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Accept"]'),
            "ios": ("","")
        }
        self.reject_button = {
            "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Reject"]'),
            "ios": ("","")
        }

    def accept_terms(self):
        self.tap(self.accept_button)
        return WelcomePage(self.driver)

    def reject_terms(self):
        self.tap(self.reject_button)
