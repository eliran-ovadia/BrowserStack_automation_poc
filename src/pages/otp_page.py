from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


class OtpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators ----------------------
        self.login_with_password_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login with Password")'),
            "ios": ("", "")
        }

    def tap_login_with_password(self):
        self.wait_and_click(self.login_with_password_button)
