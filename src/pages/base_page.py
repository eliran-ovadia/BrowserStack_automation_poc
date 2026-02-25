import logging
import os
from typing import Tuple, Union, Dict, Any

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
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
        self.window_size = None

        # ---------------- Locator resolution ----------------
    def loc(self, mapping_or_tuple: AnyLocator) -> Locator:
        """
        Accepts either:
          - {"android": (by, value), "ios": (by, value)}
          - (by, value)
          - [point_x, point_y]
        """
        if isinstance(mapping_or_tuple, tuple):
            return mapping_or_tuple
        if self.platform.startswith("ios"):
            return mapping_or_tuple["ios"]
        return mapping_or_tuple["android"]

    # ---------------- Actions ----------------
    def wait_and_click(self, locator: AnyLocator) -> None:
        loc = self.loc(locator)
        self.logger.info("tap: %s", loc)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        el.click()

    def tap_coordinates(self, coordinates: list, relative_to_window=True):
        if not self.window_size:
            self.window_size = self.driver.get_window_size()

        width = self.window_size['width']
        height = self.window_size['height']

        # 1. Safe Casting: Convert to float first to handle string inputs like "0.5", then int
        if relative_to_window:
            point_x = int(float(width) * float(coordinates[0]))
            point_y = int(float(height) * float(coordinates[1]))
        else:
            point_x = int(float(coordinates[0]))
            point_y = int(float(coordinates[1]))

        print(f"Tapping at coordinates: X={point_x}, Y={point_y}")

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(point_x, point_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

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
            print(f"could not found the locator: {loc} in time.")
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
        Scrolls a specific element until a target locator is found using modern W3C gestures.
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

        # Use wait_for_presence here, assuming it's a method in your BasePage that returns the element
        scrollable_element = self.wait_for_presence(scrollable_element_locator)

        # Determine the direction string for modern gestures
        direction = ""
        if horizontal:
            direction = "right" if opposite else "left"
        else:
            direction = "down" if opposite else "up"

        # Loop and attempt to find the element
        for i in range(max_swipes):
            try:
                # Try finding the target element within the scrollable element's context
                return scrollable_element.find_element(*target_locator)
            except NoSuchElementException:
                # If not found, execute the modern Appium gesture
                if self.platform == "android":
                    # Use mobile:swipeGesture for Android (can control speed/percent)
                    params: Dict[str, Any] = {
                        "direction": direction,
                        "elementId": scrollable_element.id,
                        "percent": 0.8,  # Swipe through X percent of the element
                        "speed": 3000  # Duration of 500ms
                    }
                    self.driver.execute_script("mobile: swipeGesture", params)
                elif self.platform == "ios":
                    # Use mobile:scroll for iOS (simpler, element-specific)
                    params: Dict[str, Any] = {
                        "direction": direction,
                        "elementId": scrollable_element.id
                    }
                    self.driver.execute_script("mobile: scroll", params)

        # If the loop finishes without finding the element, raise an exception
        raise NoSuchElementException(f"Element with locator {target_locator} not found after {max_swipes} swipes.")

    def scroll_to_and_click_locator(self, to_locator: AnyLocator, scroll_locator: AnyLocator, horizontal: bool = False, opposite = False) -> None:
        self.scroll_until_found(to_locator, scroll_locator, horizontal, opposite).click()
