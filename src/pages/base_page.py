import logging
from typing import Tuple, Union, Dict, Any

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

    def wait_for_presence(self, locator: AnyLocator, timeout: int = 0) -> WebElement | bool:
        loc = self.loc(locator)
        try:
            return self.wait.until(EC.presence_of_element_located(loc))
        except TimeoutException:
            return False

    def wait_gone(self, locator: AnyLocator) -> WebElement | bool:
        loc = self.loc(locator)
        try:
            return self.wait.until(EC.invisibility_of_element_located(loc))
        except TimeoutException:
            return False

    # ---------------- Scrolling ----------------
    def scroll_until_found(
            self,
            to_locator: AnyLocator,
            scroll_locator: AnyLocator,
            horizontal: bool = False,
            opposite: bool = False,
            max_swipes: int = 10
    ) -> WebElement:
        """
        Scrolls a specific element until a target locator is found.
        :param to_locator: The locator for the element to be found.
        :param scroll_locator: The locator for the scrollable container.
        :param horizontal: Boolean flag to enable horizontal scrolling.
        :param opposite: Boolean flag to scroll in the opposite direction.
        :param max_swipes: Maximum number of swipe attempts.
        :return: The found WebElement.
        :raises NoSuchElementException: If the element is not found after max_swipes.
        """
        target_locator = self.loc(to_locator)
        scrollable_element_locator = self.loc(scroll_locator)

        scrollable_element = self.wait_for_presence(scrollable_element_locator)
        scroll_area_size = scrollable_element.size
        scroll_area_location = scrollable_element.location

        # Determine swipe coordinates based on the scrollable element's dimensions and direction
        if horizontal:
            # Default scroll is right-to-left (content scrolls left), so start_x > end_x
            start_x = scroll_area_location['x'] + scroll_area_size['width'] * (0.2 if opposite else 0.8)
            end_x = scroll_area_location['x'] + scroll_area_size['width'] * (0.8 if opposite else 0.2)
            start_y = scroll_area_location['y'] + scroll_area_size['height'] * 0.5
            end_y = start_y
        else:  # Vertical scrolling
            # Default scroll is bottom-to-top (content scrolls up), so start_y > end_y
            start_y = scroll_area_location['y'] + scroll_area_size['height'] * (0.2 if opposite else 0.8)
            end_y = scroll_area_location['y'] + scroll_area_size['height'] * (0.8 if opposite else 0.2)
            start_x = scroll_area_location['x'] + scroll_area_size['width'] * 0.5
            end_x = start_x

        # Loop and attempt to find the element
        for i in range(max_swipes):
            try:
                return self.driver.find_element(*target_locator)
            except NoSuchElementException:
                if self.platform == "android":
                    self.driver.swipe(start_x, start_y, end_x, end_y, 200)
                elif self.platform == "ios":
                    direction = ""
                    if horizontal:
                        direction = "right" if opposite else "left"
                    else:
                        direction = "up" if opposite else "down"

                    params: Dict[str, Any] = {
                        "direction": direction,
                        "elementId": scrollable_element.id
                    }
                    self.driver.execute_script("mobile: scroll", params)

        raise NoSuchElementException(f"Element with locator {target_locator} not found after {max_swipes} swipes.")

    def scroll_to_and_click_locator(self, to_locator: AnyLocator, scroll_locator: AnyLocator, horizontal: bool = False, opposite = False) -> None:
        self.scroll_until_found(to_locator, scroll_locator, horizontal, opposite).click()
