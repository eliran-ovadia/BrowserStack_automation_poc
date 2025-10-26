from appium.webdriver.common.appiumby import AppiumBy

from src.pages.base_page import BasePage


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
            "ios": ("", "")
        }
        self.in_card_trade_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Trade").instance(0)'),
            "ios": ("", "")
        }
        self.trade_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Portfolio")'),
            "ios": ("", "")
        }
        self.fund_my_account_button_text = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fund My Account")'),
            "ios": ("", "")
        }
        self.invite_your_friend_button_text = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Invite Your Friend")'),
            "ios": ("", "")
        }
        self.currency_exchange_button_text = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Currency Exchange")'),
            "ios": ("", "")
        }
        # --------------------Demo card ----------------------
        self.in_card_demo_title = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Demo Trading").instance(0)'),
            "ios": ("", "")
        }
        self.demo_portfolio_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Demo Account")'),
            "ios": ("", "")
        }

    def nav_trade_portfolio(self):
        """
        We relay on the "My Portfolio" text to enter trade.
        When we cannot enter Trade, we get a different text such as "go to nextgen" ect...
        """
        self.tap(self.trade_portfolio_button)

    def nav_demo(self):  # Capabilities demonstration only
        self.scroll_to_and_click_locator(self.demo_portfolio_button, horizontal=True)

    def nav_profile(self):
        self.tap(self.profile_button)

    def nav_settings(self):
        self.tap(self.settings_button)

    def nav_fund_my_account(self):
        self.tap(self.fund_my_account_button_text)

    def nav_invite_your_friend(self):
        self.tap(self.invite_your_friend_button_text)

    def nav_currency_exchange(self):
        self.tap(self.currency_exchange_button_text)
