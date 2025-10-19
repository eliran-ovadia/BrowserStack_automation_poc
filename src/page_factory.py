from typing import Type, Literal
from src.pages.base_page import BasePage
from src.pages import PAGE_REGISTRY, PAGE_LITERAL


class PageFactory:
    def __init__(self, driver):
        self.driver = driver
        self.registry: dict[str, Type[BasePage]] = dict(PAGE_REGISTRY)


    def get_page(self, name: PAGE_LITERAL) -> BasePage:
        try:
            cls = self.registry[name]
        except KeyError:
            raise ValueError(f"Unknown page: {name}. Options: {list(self.registry)}")
        return cls(self.driver)
