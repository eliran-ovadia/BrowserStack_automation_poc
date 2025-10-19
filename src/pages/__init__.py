from typing import Literal

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


PAGE_REGISTRY = {
    "currency_exchange": CurrencyExchangePage,
    "dashboard": DashboardPage,
    "edit_order": EditOrderPage,
    "forgot_password": ForgotPasswordPage,
    "fund_my_account": FundMyAccountPage,
    "invite_your_friend": InviteYourFriendPage,
    "knowledge": KnowledgePage,
    "login_with_password": LoginWithPasswordPage,
    "market": MarketPage,
    "orders": OrdersPage,
    "otp": OtpPage,
    "portfolio_analysis": PortfolioAnalysisPage,
    "portfolio": PortfolioPage,
    "profile": ProfilePage,
    "search": SearchPage,
    "sending_order": SendingOrderPage,
    "settings": SettingsPage,
    "stock": StockPage,
    "terms": TermsPage,
    "tipranks_analyst": TipranksAnalystPage,
    "tipranks_top_analysts": TipranksTopAnalystsPage,
    "watchlist": WatchlistPage,
    "welcome": WelcomePage,
}


PAGE_LITERAL = Literal[
    "currency_exchange",
    "dashboard",
    "edit_order",
    "forgot_password",
    "fund_my_account",
    "invite_your_friend",
    "knowledge",
    "login_with_password",
    "market",
    "orders",
    "otp",
    "portfolio_analysis",
    "portfolio",
    "profile",
    "search",
    "sending_order",
    "settings",
    "stock",
    "terms",
    "tipranks_analyst",
    "tipranks_top_analysts",
    "watchlist",
    "welcome",
]
