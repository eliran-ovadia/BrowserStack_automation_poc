import logging
from typing import Tuple, Union, Dict

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = True

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

    # TODO: This is a preparation for a dual platform back method, at the moment, I will use driver.back() for android
    # def press_back(self):
    #     if self.platform.startswith("android"):
    #         self.logger.info("Pressing Android BACK button")
    #         self.driver.press_keycode(AndroidKey.BACK)
    #     else:
    #         self.logger.warning("press_back() not implemented for platform: %s", self.platform)

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

    def scroll_to_text(self, text: str, scroll_locator: AnyLocator, horizontal: bool = False) -> WebElement:
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

    # TODO: refactor this function to utilize a loop to swipe and check for element on the screen
    def scroll_until_found(self, to_locator: AnyLocator, scroll_locator: AnyLocator, horizontal: bool = False, max_swipes: int = 10) -> WebElement:
        # First, we take the locators themselves from the tuple of each AnyLocator
        locator = self.loc(to_locator)
        scroll_locator = self.loc(scroll_locator)

        # We will loop the maximum amount of swipes, every time we cannot find the locator, we will scroll the page
        for i in range(max_swipes):
            try:
                return self.driver.find_element(*locator)
            except NoSuchElementException:
                if self.platform == "android":
                    # Perform a swipe up for Android
                    size = self.driver.get_window_size()
                    start_y = size['height'] * 0.8
                    end_y = size['height'] * 0.2
                    center_x = size['width'] * 0.5
                    self.driver.swipe(center_x, start_y, center_x, end_y, 800)
                elif self.platform == "ios":
                    # Use mobile:scroll gesture for iOS
                    params = {"direction": "down", "distance": 0.5}
                    self.driver.execute_script("mobile: scroll", params)

        # We raise if we scrolled the maximum amount but have not fond the locator
        raise NoSuchElementException(f"Element with locator {locator} not found after {max_swipes} swipes.")

    def scroll_to_and_click_text(self, text: str, scroll_locator: AnyLocator, horizontal: bool = False) -> None:
        self.scroll_to_text(text, scroll_locator, horizontal).click()

    def scroll_to_and_click_locator(self, to_locator: AnyLocator, scroll_locator: AnyLocator, horizontal: bool = False) -> None:
        self.scroll_until_found(to_locator, scroll_locator, horizontal).click()
