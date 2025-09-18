# pages/base_page.py
import logging
from typing import Tuple

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.platform = (driver.capabilities.get("platformName") or "").lower()
        # Logger
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.logger.info("Initializing base page, platform: %s", self.platform)


    def loc(self, mapping_or_tuple):
        """
        Accepts either:
          - a dict like {"android": (by, value), "ios": (by, value)}
          - or a direct (by, value) tuple (returned as-is)
        """
        # If the caller passed a raw (by, value) tuple, just use it.
        if isinstance(mapping_or_tuple, tuple):
            return mapping_or_tuple

        # Otherwise choose by platform
        if self.platform.startswith("ios"):
            return mapping_or_tuple["ios"]
        return mapping_or_tuple["android"]  # default branch


    # ---------- Element Interactions ----------
    def tap(self, locator: dict | Tuple[str, str]) -> None:
        """ Tap an element on the page """
        loc = self.loc(locator)
        self.logger.info(f"tap: Clicking element: {loc}")
        el = self.wait.until(EC.visibility_of_element_located(loc)) # Wait for clickable not visible, will keep an eye
        el.click()

    def write(self, locator: dict | Tuple[str, str], text: str) -> None:
        """ Write to a textbox"""
        loc = self.loc(locator)
        self.logger.info(f"Typing '{text}' into: {loc}")
        el = self.wait.until(EC.visibility_of_element_located(loc))
        el.clear()
        el.send_keys(text)

    def is_visible(self, locator: dict | Tuple[str, str]) -> bool:
        loc = self.loc(locator)
        try:
            self.wait.until(EC.visibility_of_element_located(loc))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator: dict | Tuple[str, str]) -> str:
        """ Given a locator, return the text it contains"""
        loc = self.loc(locator)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        return el.text

    def find_element(self, locator: dict | Tuple[str, str]) -> WebElement:
        """ Wait for an element to be locatable by presence(not explicitly visible)"""
        loc = self.loc(locator)
        return self.wait.until(EC.presence_of_element_located(loc))

    # ---------- Scrolling ----------
    def scroll_to_text(self, text: str, horizontal: bool = False) -> WebElement:
        self.logger.info(f"Scrolling to text: {text}")
        scrollable = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'{".setAsHorizontalList()" if horizontal else ""}'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )
        return self.driver.find_element(*scrollable)  # We rely on UiScrollable for waiting until finding the element

    def scroll_to_locator(self, locator: dict | Tuple[str, str], horizontal: bool = False) -> WebElement:
        loc = self.loc(locator)
        self.logger.info(f"Scrolling to locator: {locator}")
        scrollable = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'{".setAsHorizontalList()" if horizontal else ""}'
            f'.scrollIntoView({loc[1]})'
        )
        return self.driver.find_element(*scrollable)  # We rely on UiScrollable for waiting until finding the element

    def scroll_to_and_click_text(self, text: str, horizontal: bool = False) -> None:
        el = self.scroll_to_text(text, horizontal)
        el.click()

    def scroll_to_and_click_locator(self, locator: dict | Tuple[str, str], horizontal: bool = False) -> None:
        loc = self.loc(locator)
        el = self.scroll_to_locator(loc, horizontal)
        el.click()
