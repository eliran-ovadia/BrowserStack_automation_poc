from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.market_page import MarketPage
from src.pages.orders_page import OrdersPage
from src.pages.profile_page import ProfilePage
from src.pages.knowledge_page import KnowledgePage

class SearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # ------------ Locators ---------------
        self.orders_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Orders")'),
            "ios": ("","")
        }
        self.knowledge_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Knowledge")'),
            "ios": ("","")
        }
        self.portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Portfolio")'),
            "ios": ("","")
        }
        self.market_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Market")'),
            "ios": ("","")
        }

    def enter_orders_page(self) -> OrdersPage:
        self.tap(self.orders_button)
        orders = OrdersPage(self.driver)
        return orders

    def enter_knowledge_page(self) -> KnowledgePage:
        self.tap(self.knowledge_button)
        knowledge = KnowledgePage(self.driver)
        return knowledge

    def enter_profile_page(self) -> ProfilePage:
        self.tap(self.portfolio_button)
        profile = ProfilePage(self.driver)
        return profile

    def enter_market_page(self) -> MarketPage:
        self.tap(self.market_button)
        market = MarketPage(self.driver)
        return market
