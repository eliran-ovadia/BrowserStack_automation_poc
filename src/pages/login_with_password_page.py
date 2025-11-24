import os

from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class LoginWithPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.password = os.getenv('PASSWORD')
        # Locators ----------------------
        self.forgot_password_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Forgot password?")'),
            "ios": ("", "")
        }
        self.password_input_field = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'),
            "ios": (AppiumBy.XPATH, '//XCUIElementTypeTextField[@value="input your password"]')
        }
        self.login_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")'),
            "ios": (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Login"]')
        }

    def enter_password(self):
        self.write(self.password_input_field, self.password)
        self.logger.info(f"Entered password: {self.password}")
        return self

    def tap_password_login(self):
        self.wait_and_click(self.login_button)
        self.logger.info("Tapped Login on password page")
