from appium.webdriver.common.appiumby import AppiumBy

from src.components.navbar import NavBar
from src.pages.base_page import BasePage


class PortfolioPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.navbar = NavBar(self.tap)
        # Locators -----------------
        self.scroll_view = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ScrollView")'),
            "ios": ("", "")
        }
        self.portfolio_analysis_show_me_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Show me")'),
            "ios": ("", "")
        }
        # --------------------------

    def enter_portfolio_analysis(self):
        self.scroll_to_and_click_locator(self.portfolio_analysis_show_me_button, self.scroll_view)

