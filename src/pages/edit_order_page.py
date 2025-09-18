from src.flows.base_flow import BaseFlow


class EditOrderPage(BaseFlow):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
