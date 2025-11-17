from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.services.get_strings import get_strings


class TermsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        strings = get_strings("dashboard_profile")
        # Locators ----------------------
        self.accept_button = {
            "android": (AppiumBy.XPATH, f'//android.widget.TextView[@text="{strings["dashboard_profile_terms_approve"]["English"]}"]'),
            "ios": ("", "")
        }
        self.reject_button = {
            "android": (AppiumBy.XPATH, f'//android.widget.TextView[@text="{strings["dashboard_profile_terms_reject"]["English"]}"]'),
            "ios": ("", "")
        }

    def accept_terms(self):
        self.tap(self.accept_button)

    def reject_terms(self):
        self.tap(self.reject_button)
