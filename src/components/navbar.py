from appium.webdriver.common.appiumby import AppiumBy


class NavBar:
    """Bottom navigation bar for Trade bottom section (portfolio, market, search, orders, knowledge"""
    def __init__(self, tap_fn):
        self.tap = tap_fn
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

    def tap_portfolio(self):
        self.tap(self.portfolio_button)

    def tap_market(self):
        self.tap(self.market_button)

    def tap_search(self):
        self.tap(self.search_button)

    def tap_orders(self):
        self.tap(self.orders_button)

    def tap_knowledge(self):
        self.tap(self.knowledge_button)
