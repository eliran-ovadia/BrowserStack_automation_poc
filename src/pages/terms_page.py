from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.api_utils.get_strings import get_strings


class TermsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        strings = get_strings("dashboard_profile")
        # Locators ----------------------
        self.accept_button = {
            "android": (AppiumBy.XPATH, f'//android.widget.TextView[@text="{strings["dashboard_profile_terms_approve"]["English"]}"]'),
            "ios": (AppiumBy.XPATH, f'//XCUIElementTypeStaticText[@name="{strings["dashboard_profile_terms_approve"]["English"]}"]')
        }
        self.reject_button = {
            "android": (AppiumBy.XPATH, f'//android.widget.TextView[@text="{strings["dashboard_profile_terms_reject"]["English"]}"]'),
            "ios": (AppiumBy.XPATH, f'//XCUIElementTypeStaticText[@name="{strings["dashboard_profile_terms_reject"]["English"]}"]')
        }

    def accept_terms(self):
        self.wait_and_click(self.accept_button)

    def reject_terms(self):
        self.wait_and_click(self.reject_button)
