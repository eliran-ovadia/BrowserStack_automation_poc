from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.market_page import MarketPage
from src.pages.orders_page import OrdersPage
from src.pages.profile_page import ProfilePage
from src.pages.search_page import SearchPage


class KnowledgePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # --------- Locators ---------------------
        self.market_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Market")'),
            "ios": ("","")
        }
        self.search_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(4)'),
            "ios": ("","")
        }
        self.orders_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Orders")'),
            "ios": ("","")
        }
        self.portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Portfolio")'),
            "ios": ("","")
        }


    def enter_market_page(self) -> MarketPage:
        self.tap(self.market_button)
        market = MarketPage(self.driver)
        return market

    def enter_search_page(self) -> SearchPage:
        self.tap(self.search_button)
        search = SearchPage(self.driver)
        return search

    def enter_orders_page(self) -> OrdersPage:
        self.tap(self.orders_button)
        orders = OrdersPage(self.driver)
        return orders

    def enter_profile_page(self) -> ProfilePage:
        self.tap(self.portfolio_button)
        profile = ProfilePage(self.driver)
        return profile
