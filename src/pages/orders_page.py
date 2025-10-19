from src.components.navbar import NavBar
from src.pages.base_page import BasePage


class OrdersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.navbar = NavBar(self.tap)
        # ------------ Locators ----------------
        # --------------------------------------
