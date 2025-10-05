from src.pages.base_page import BasePage

from appium.webdriver.common.appiumby import AppiumBy
from src.pages.orders_page import OrdersPage
from src.pages.profile_page import ProfilePage
from src.pages.search_page import SearchPage
from src.pages.knowledge_page import KnowledgePage


class MarketPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # ------------ Locators ----------------
        self.portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Portfolio")'),
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
        self.knowledge_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Knowledge")'),
            "ios": ("","")
        }

    def enter_search_page(self) -> SearchPage:
        self.tap(self.search_button)
        search = SearchPage(self.driver)
        return search

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
