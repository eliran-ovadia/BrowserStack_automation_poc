from appium.webdriver.common.appiumby import AppiumBy
from src.pages.base_page import BasePage


class NavBar(BasePage):
    """Bottom navigation bar for Trade bottom section (portfolio, market, search, orders, knowledge"""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # --- Locators ---------------------
        self.portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Portfolio")'),
            "ios": ("", "")
        }
        self.market_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Market")'),
            "ios": ("", "")
        }
        self.search_button = {
            "android": ('', ''),
            "ios": (AppiumBy.XPATH, '//XCUIElementTypeImage[@name="ic_tab_bar_search"]')
        }
        self.orders_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Orders")'),
            "ios": ("", "")
        }
        self.knowledge_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Knowledge")'),
            "ios": ("", "")
        }

    def tap_portfolio(self):
        self.wait_and_click(self.portfolio_button)

    def tap_market(self):
        self.wait_and_click(self.market_button)

    # I commented this method, because the search locator is not consistent across all pages that utilize it
    # TODO: Request an accessibility id or a test-tag to have an explicit locator for the search button
    def tap_search(self):
        self.wait_for_presence(self.market_button)
        if self.platform == "android":
            self.tap_coordinates([0.5, 0.90]) # The search button is always at the same place (relative)
        else:
            self.wait_and_click(self.search_button)

    def tap_orders(self):
        self.wait_and_click(self.orders_button)

    def tap_knowledge(self):
        self.wait_and_click(self.knowledge_button)
