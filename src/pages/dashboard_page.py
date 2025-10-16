from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage
from src.pages.currency_exchange_page import CurrencyExchangePage
from src.pages.fund_my_account_page import FundMyAccountPage
from src.pages.invite_your_friend_page import InviteYourFriendPage
from src.pages.portfolio_page import PortfolioPage
from src.pages.profile_page import ProfilePage
from src.pages.settings_page import SettingsPage


class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators ------------------------
        self.profile_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.Button").instance(1)'),
            "ios": ("", "")
        }
        self.settings_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.Button").instance(2)'),
            "ios": ("", "")
        }
        # ---------------------Trade card ----------------------
        self.scrollable_dashboard_element = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(2)'),
            "ios": ("","")
        }
        self.in_card_trade_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Trade").instance(0)'),
            "ios": ("","")
        }
        self.trade_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Portfolio")'),
            "ios": ("", "")
        }
        self.fund_my_account_button_text = {
            "android" : (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fund My Account")'),
            "ios": ("", "")
        }
        self.invite_your_friend_button_text = {
            "android" : (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Invite Your Friend")'),
            "ios": ("", "")
        }
        self.currency_exchange_button_text = {
            "android" : (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Currency Exchange")'),
            "ios": ("", "")
        }
        # --------------------Demo card ----------------------
        self.in_card_demo_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Demo Trading").instance(0)'),
            "ios": ("","")
        }
        self.demo_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Demo Account")'),
            "ios": ("","")
        }

    def enter_trade(self) -> PortfolioPage:
        """
        We relay on the "My Portfolio" text to enter trade.
        When we cannot enter Trade, we get a different text such as "go to nextgen" ect...
        :return: portfolioPage
        """
        self.tap(self.trade_portfolio_button)
        portfolio = PortfolioPage(self.driver)
        return portfolio

    def enter_demo(self): # Capabilities demonstration only
        self.scroll_to_locator(self.demo_portfolio_button, horizontal=True)
        self.tap(self.demo_portfolio_button)

    def enter_profile(self) -> ProfilePage:
        self.tap(self.profile_button)
        profile = ProfilePage(self.driver)
        return profile

    def enter_settings(self) -> SettingsPage:
        self.tap(self.settings_button)
        settings = SettingsPage(self.driver)
        return settings

    def enter_fund_my_account(self) -> FundMyAccountPage:
        self.tap(self.fund_my_account_button_text)
        fund_my_account = FundMyAccountPage(self.driver)
        return fund_my_account

    def enter_invite_your_friend(self) -> InviteYourFriendPage:
        self.tap(self.invite_your_friend_button_text)
        invite_your_friend = InviteYourFriendPage(self.driver)
        return invite_your_friend

    def enter_currency_exchange(self) -> CurrencyExchangePage:
        self.tap(self.currency_exchange_button_text)
        currency_exchange = CurrencyExchangePage(self.driver)
        return currency_exchange
