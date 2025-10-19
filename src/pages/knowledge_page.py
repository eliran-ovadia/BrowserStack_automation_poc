from appium.webdriver.common.appiumby import AppiumBy

from src.components.navbar import NavBar
from src.page_factory import PageFactory

from src.pages.base_page import BasePage
from src.pages.market_page import MarketPage
from src.pages.orders_page import OrdersPage
from src.pages.profile_page import ProfilePage
from src.pages.search_page import SearchPage


class KnowledgePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.navbar = NavBar(self.driver, getattr(self, self.tap))
        # --------- Locators ---------------------


    def enter_market_page(self) -> MarketPage:
        self.navbar.navigate_to("market")
        market = MarketPage(self.driver)
        return market

    def enter_search_page(self) -> SearchPage:
        self.navbar.navigate_to("search")
        search = SearchPage(self.driver)
        return search

    def enter_orders_page(self) -> OrdersPage:
        self.navbar.navigate_to("orders")
        orders = OrdersPage(self.driver)
        return orders

    def enter_portfolio_page(self) -> ProfilePage:
        self.navbar.navigate_to("portfolio")
        profile = ProfilePage(self.driver)
        return profile
