# src/pages/base_page.py
import logging
from typing import Tuple, Union, Dict

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]
PlatMapped = Dict[str, Locator]
AnyLocator = Union[Locator, PlatMapped]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.platform = (driver.capabilities.get("platformName") or "").lower()

        # Logger (avoid duplicate handlers across reloads)
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            ))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.logger.info("Init %s (platform=%s)", self.__class__.__name__, self.platform)

    # ---------------- Locator resolution ----------------
    def loc(self, mapping_or_tuple: AnyLocator) -> Locator:
        """
        Accepts either:
          - {"android": (by, value), "ios": (by, value)}
          - (by, value)
        """
        if isinstance(mapping_or_tuple, tuple):
            return mapping_or_tuple
        if self.platform.startswith("ios"):
            return mapping_or_tuple["ios"]
        return mapping_or_tuple["android"]

    # ---------------- Actions ----------------
    def tap(self, locator: AnyLocator) -> None:
        loc = self.loc(locator)
        self.logger.info("tap: %s", loc)
        el = self.wait.until(EC.element_to_be_clickable(loc))
        el.click()

    def write(self, locator: AnyLocator, text: str, clear: bool = True) -> None:
        loc = self.loc(locator)
        self.logger.info("write: %s -> %r", loc, text)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        if clear:
            el.clear()
        el.send_keys(text)

    def read(self, locator: AnyLocator) -> str:
        loc = self.loc(locator)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        return el.text

    # ---------------- Checks ----------------
    def is_visible(self, locator: AnyLocator, timeout: int = 0) -> bool:
        loc = self.loc(locator)
        try:
            (self.wait if timeout == 0 else WebDriverWait(self.driver, timeout)) \
                .until(EC.visibility_of_element_located(loc))
            return True
        except TimeoutException:
            return False

    def is_present(self, locator: AnyLocator, timeout: int = 0) -> bool:
        loc = self.loc(locator)
        try:
            (self.wait if timeout == 0 else WebDriverWait(self.driver, timeout)) \
                .until(EC.presence_of_element_located(loc))
            return True
        except TimeoutException:
            return False

    def wait_gone(self, locator: AnyLocator) -> bool:
        loc = self.loc(locator)
        try:
            return self.wait.until(EC.invisibility_of_element_located(loc))
        except TimeoutException:
            return False

    # ---------------- Scrolling (Android UiScrollable) ----------------
    def _ensure_android(self):
        if not self.platform.startswith("android"):
            raise NotImplementedError("UiScrollable is Android-only")

    def scroll_to_text(self, text: str, horizontal: bool = False) -> WebElement:
        """
        Scrolls until a view with exact text() is visible; returns the found element.
        Android only.
        """
        self._ensure_android()
        self.logger.info("scroll_to_text: %r (horizontal=%s)", text, horizontal)
        scrollable = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            + (".setAsHorizontalList()" if horizontal else "")
            + f'.scrollIntoView(new UiSelector().text("{text}"))'
        )
        return self.driver.find_element(*scrollable)

    def scroll_to_locator(self, to_locator: AnyLocator, horizontal: bool = False) -> WebElement:
        """
        Scrolls until a UiAutomator2 locator is brought into view; returns the found element.
        NOTE: to_locator MUST be (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector()...')
        """
        self._ensure_android()
        loc = self.loc(to_locator)
        if loc[0] != AppiumBy.ANDROID_UIAUTOMATOR or "new UiSelector()" not in loc[1]:
            raise ValueError(
                "scroll_to_locator requires an ANDROID_UIAUTOMATOR locator with a 'new UiSelector()' expression"
            )
        self.logger.info("scroll_to_locator: %s (horizontal=%s)", loc, horizontal)
        scrollable = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            + (".setAsHorizontalList()" if horizontal else "")
            + f".scrollIntoView({loc[1]})"
        )
        # Execute the UiScrollable expression and return the element that was brought into view
        return self.driver.find_element(*scrollable)

    def scroll_to_and_tap_text(self, text: str, horizontal: bool = False) -> None:
        self.scroll_to_text(text, horizontal).click()

    def scroll_to_and_tap_locator(self, to_locator: AnyLocator, horizontal: bool = False) -> None:
        self.scroll_to_locator(to_locator, horizontal).click()
