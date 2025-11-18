import os

from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.services.get_strings import get_strings


class WelcomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username = os.getenv("USER")
        strings = get_strings("dashboard_profile")
        # Locators ----------------------
        self.username_field = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'),
            "ios": ("", "")
        }
        self.login_button = {
            "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Login"]'),
            "ios": ("", "")
        }

    def enter_username(self):
        self.write(self.username_field, self.username)
        self.logger.info(f"Entered username: {self.username}")
        return self

    def tap_welcome_login(self):
        self.wait_and_click(self.login_button)
        self.logger.info(f"Tapped login button")
