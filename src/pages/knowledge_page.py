from src.components.navbar import NavBar

from src.pages.base_page import BasePage
from src.page_factory import PageFactory


class KnowledgePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.navbar = NavBar(self.tap)
        self.page_factory = PageFactory(self.driver)
        # --------- Locators ---------------------

        # ----------------------------------------

    def enter_portfolio(self) -> BasePage:
        self.navbar.tap_portfolio()
        portfolio = self.page_factory.get_page("portfolio")
        return portfolio

    def enter_market(self) -> BasePage:
        self.navbar.tap_market()
        market = self.page_factory.get_page("market")
        return market

    def enter_search(self) -> BasePage:
        self.navbar.tap_search()
        search = self.page_factory.get_page("search")
        return search

    def enter_orders(self) -> BasePage:
        self.navbar.tap_orders()
        orders = self.page_factory.get_page("orders")
        return orders
