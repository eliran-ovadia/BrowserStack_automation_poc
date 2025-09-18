from src.flows.base_flow import BaseFlow


class WatchlistPage(BaseFlow):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
