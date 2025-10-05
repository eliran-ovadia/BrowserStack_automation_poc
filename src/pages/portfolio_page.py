from src.flows.base_flow import BaseFlow
from appium.webdriver.common.appiumby import AppiumBy

class PortfolioPage(BaseFlow):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # Locators -----------------
        # Nav bar ------------------
        self.market_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Market")'),
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
