from typing import Literal

from appium.webdriver.common.appiumby import AppiumBy

class NavBar:
    """Bottom navigation bar for Trade bottom section (portfolio, market, search, orders, knowledge"""
    def __init__(self, driver, tap_fn):
        self.driver = driver
        self.tap_fn = tap_fn
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
            "android": (AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.Button").instance(4)'),
            "ios": ("", "")
        }
        self.orders_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Orders")'),
            "ios": ("", "")
        }
        self.knowledge_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Knowledge")'),
            "ios": ("","")
        }

    # todo: convert to regular more verbose functions instead of dynamically getattr
    def navigate_to(self, to_page: Literal["portfolio", "market", "search", "orders", "knowledge"]):
        page = getattr(self, f"{to_page}_button")
        self.tap_fn(page)
