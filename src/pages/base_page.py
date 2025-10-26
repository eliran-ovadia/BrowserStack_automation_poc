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

    def scroll_until_found(
            self,
            hidden_locator: AnyLocator,
            scroll_locator: AnyLocator,
            horizontal: bool = False,
            max_swipes: int = 10
    ) -> WebElement:
        """
        Scrolls a specific element until a target locator is found.
        :param hidden_locator: The locator for the element to be found.
        :param scroll_locator: The locator for the scrollable container.
        :param horizontal: Boolean flag to enable horizontal scrolling.
        :param max_swipes: Maximum number of swipe attempts.
        :return: The found WebElement.
        :raises NoSuchElementException: If the element is not found after max_swipes.
        """
        # First, get the locator values from the tuples
        target_locator = self.loc(hidden_locator)
        scrollable_element_locator = self.loc(scroll_locator)

        # Get the scrollable element once
        scrollable_element = self.driver.find_element(*scrollable_element_locator)
        scroll_area_size = scrollable_element.size
        scroll_area_location = scrollable_element.location

        # Determine swipe coordinates based on the scrollable element's dimensions
        if horizontal:
            start_x = scroll_area_location['x'] + scroll_area_size['width'] * 0.8
            end_x = scroll_area_location['x'] + scroll_area_size['width'] * 0.2
            y = scroll_area_location['y'] + scroll_area_size['height'] * 0.5
            start_y = end_y = y  # Vertical position remains constant
        else:  # Vertical scrolling
            x = scroll_area_location['x'] + scroll_area_size['width'] * 0.5
            start_y = scroll_area_location['y'] + scroll_area_size['height'] * 0.8
            end_y = scroll_area_location['y'] + scroll_area_size['height'] * 0.2
            start_x = end_x = x  # Horizontal position remains constant

        # Loop and attempt to find the element
        for i in range(max_swipes):
            try:
                return self.driver.find_element(*target_locator)
            except NoSuchElementException:
                if self.platform == "android":
                    self.driver.swipe(start_x, start_y, end_x, end_y, 800)
                elif self.platform == "ios":
                    # For iOS, use the 'mobile:scroll' gesture which can be more reliable.
                    # However, for scrolling a specific element, the W3C Actions API is better.
                    # This example uses a simplified approach for demonstration.
                    params = {
                        "direction": "left" if horizontal else "down",
                        "element": scrollable_element.id
                    }
                    self.driver.execute_script("mobile: scroll", params)

        # If the loop finishes without finding the element, raise an exception
        raise NoSuchElementException(f"Element with locator {target_locator} not found after {max_swipes} swipes.")

    def scroll_to_and_click_text(self, text: str, scroll_locator: AnyLocator, horizontal: bool = False) -> None:
        self.scroll_to_text(text, scroll_locator, horizontal).click()

    def scroll_to_and_click_locator(self, to_locator: AnyLocator, scroll_locator: AnyLocator, horizontal: bool = False) -> None:
        self.scroll_until_found(to_locator, scroll_locator, horizontal).click()
