from appium.webdriver.common.appiumby import AppiumBy


class MoreActions:
    """More actions pull down menu in Trade - contain: Fund My Account, Withdrawal, Credit, Currency Exchange,
        More Self Service Options, Price Alerts, Recurring Investment"""
    def __init__(self, tap_fn):
        self.tap = tap_fn
        # --- Locators ---------------------
        self.close_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button")'),
            "ios": ("", "")
        }
        self.fund_my_account_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fund My Account")'),
            "ios": ("", "")
        }
        self.withdrawal_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Withdrawal")'),
            "ios": ("", "")
        }
        self.credit_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Credit (Leverage")'),
            "ios": ("", "")
        }
        self.currency_exchange_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Currency Exchange")'),
            "ios": ("", "")
        }
        self.more_self_service_options_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("More Self Service Options")'),
            "ios": ("", "")
        }
        self.price_alerts_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Price Alerts")'),
            "ios": ("", "")
        }
        self.recurring_investment_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Recurring Investment")'),
            "ios": ("", "")
        }
        self.more_info_button = {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("More Info")'),
            "ios": ("", "")
        }
        # TODO: At the moment, i cannot locate the whatsapp hyper-text (just like in the terms page)
        # self.whatsapp_button = {
        #     "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fund My Account")'),
        #     "ios": ("", "")
        # }

    def nav_fund_my_account(self):
        self.tap(self.fund_my_account_button)

    def nav_withdrawal(self):
        self.tap(self.withdrawal_button)

    def nav_credit(self):
        self.tap(self.credit_button)

    def nav_currency_exchange(self):
        self.tap(self.currency_exchange_button)

    def nav_more_self_service(self):
        self.tap(self.more_self_service_options_button)

    def nav_price_alerts(self):
        self.tap(self.price_alerts_button)

    def nav_recurring_investment(self):
        self.tap(self.recurring_investment_button)

    def nav_more_info(self):
        self.tap(self.more_info_button)
