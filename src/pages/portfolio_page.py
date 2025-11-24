from appium.webdriver.common.appiumby import AppiumBy
from src.components.top_menu_shutter import TopMenuShutter
from src.pages.base_page import BasePage


class PortfolioPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.more_actions = TopMenuShutter(self.wait_and_click)
        # Locators -----------------
        self.scroll_view = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ScrollView")'),
            "ios": (AppiumBy.XPATH, '//XCUIElementTypeTable')
        }
        self.home_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)'),
            "ios": ("", "")
        }
        self.watchlist_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(3)'),
            "ios": ("", "")
        }
        self.portfolio_analysis_show_me_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Show me")'),
            "ios": (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Show me"]')
        }
        # --------------------------

    def enter_portfolio_analysis(self):
        self.scroll_to_and_click_locator(self.portfolio_analysis_show_me_button, self.scroll_view)

    def nav_dashboard(self):
        self.wait_and_click(self.home_button)

    def open_more_actions(self):
        pass

    def nav_watchlist(self):
        self.wait_and_click(self.home_button)

