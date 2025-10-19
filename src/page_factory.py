from src.pages.currency_exchange_page import CurrencyExchangePage
from src.pages.dashboard_page import DashboardPage
from src.pages.edit_order_page import EditOrderPage
from src.pages.forgot_password_page import ForgotPasswordPage
from src.pages.fund_my_account_page import FundMyAccountPage
from src.pages.invite_your_friend_page import InviteYourFriendPage
from src.pages.knowledge_page import KnowledgePage
from src.pages.login_with_password_page import LoginWithPasswordPage
from src.pages.market_page import MarketPage
from src.pages.orders_page import OrdersPage
from src.pages.otp_page import OtpPage
from src.pages.portfolio_analysis_page import PortfolioAnalysisPage
from src.pages.portfolio_page import PortfolioPage
from src.pages.profile_page import ProfilePage
from src.pages.search_page import SearchPage
from src.pages.sending_order_page import SendingOrderPage
from src.pages.settings_page import SettingsPage
from src.pages.stock_page import StockPage
from src.pages.terms_page import TermsPage
from src.pages.tipranks_analyst_page import TipranksAnalystPage
from src.pages.tipranks_top_analysts_page import TipranksTopAnalystsPage
from src.pages.watchlist_page import WatchlistPage
from src.pages.welcome_page import WelcomePage


class PageFactory:
    def __init__(self, driver):
        self.driver = driver

    # ---------- Explicit helpers (typed, IDE-friendly) ----------
    def currency_exchange(self) -> CurrencyExchangePage: return CurrencyExchangePage(self.driver)

    def dashboard(self) -> DashboardPage: return DashboardPage(self.driver)

    def edit_order(self) -> EditOrderPage: return EditOrderPage(self.driver)

    def forgot_password(self) -> ForgotPasswordPage: return ForgotPasswordPage(self.driver)

    def fund_my_account(self) -> FundMyAccountPage: return FundMyAccountPage(self.driver)

    def invite_your_friend(self) -> InviteYourFriendPage: return InviteYourFriendPage(self.driver)

    def knowledge(self) -> KnowledgePage: return KnowledgePage(self.driver)

    def login_with_password(self) -> LoginWithPasswordPage: return LoginWithPasswordPage(self.driver)

    def market(self) -> MarketPage: return MarketPage(self.driver)

    def orders(self) -> OrdersPage: return OrdersPage(self.driver)

    def otp(self) -> OtpPage: return OtpPage(self.driver)

    def portfolio_analysis(self) -> PortfolioAnalysisPage: return PortfolioAnalysisPage(self.driver)

    def portfolio(self) -> PortfolioPage: return PortfolioPage(self.driver)

    def profile(self) -> ProfilePage: return ProfilePage(self.driver)

    def search(self) -> SearchPage: return SearchPage(self.driver)

    def sending_order(self) -> SendingOrderPage: return SendingOrderPage(self.driver)

    def settings(self) -> SettingsPage: return SettingsPage(self.driver)

    def stock(self) -> StockPage: return StockPage(self.driver)

    def terms(self) -> TermsPage: return TermsPage(self.driver)

    def tipranks_analyst(self) -> TipranksAnalystPage: return TipranksAnalystPage(self.driver)

    def tipranks_top_analysts(self) -> TipranksTopAnalystsPage: return TipranksTopAnalystsPage(self.driver)

    def watchlist(self) -> WatchlistPage: return WatchlistPage(self.driver)

    def welcome(self) -> WelcomePage: return WelcomePage(self.driver)
