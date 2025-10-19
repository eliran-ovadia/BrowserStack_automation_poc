from src.pages.base_page import BasePage


class TipranksAnalystPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
