from typing import Literal

from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.portfolio_page import PortfolioPage


class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators ------------------------
        # Trade card ----------------------
        self.user_button = {
                "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)'),
                "ios": ("","")
            }
        self.settings_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(2)'),
            "ios": ("","")
        }
        self.scrollable_dashboard_element = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(2)'),
            "ios": ("","")
        }
        self.in_card_trade_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Trade").instance(0)'),
            "ios": ("","")
        }
        self.Trade_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Portfolio")'),
            "ios": ("", "")
        }
        # Demo card ----------------------
        self.in_card_demo_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Demo Trading").instance(0)'),
            "ios": ("","")
        }
        self.demo_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Demo Account")'),
            "ios": ("","")
        }

    def enter_trade(self) -> PortfolioPage:
        self.tap(self.Trade_portfolio_button)
        portfolio = PortfolioPage(self.driver)
        return portfolio

    def enter_demo(self):
        self.scroll_to_and_click_locator(self.demo_portfolio_button, horizontal=True)
