import os

from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.dashboard_page import DashboardPage


class LoginWithPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.password = os.getenv('PASSWORD')
        # Locators ----------------------
        self.forgot_password_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Forgot password?")'),
            "ios": ("","")
        }
        self.password_input_field = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'),
            "ios": ("","")
        }
        self.login_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")'),
            "ios": ("","")
        }


    def enter_password(self):
        self.write(self.password_input_field, self.password)
        self.logger.info(f"Entered password: {self.password}")
        return self

    def tap_password_login(self):
        self.tap(self.login_button)
        self.logger.info("Tapped Login on password page")
        return DashboardPage(self.driver)
