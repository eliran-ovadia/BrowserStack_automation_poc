import os

import dotenv
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

dotenv.load_dotenv()
platform = os.getenv("TEST_PLATFORM").lower()
# @pytest.fixture(scope='function')
# def set_web_driver(request, session_capabilities):
#     remoteURL = "https://hub.browserstack.com/wd/hub"
#     driver = webdriver.Remote(remoteURL, session_capabilities)
#     request.instance.driver = driver
#     request.node._driver = driver
#     yield driver
#     driver.quit()


# ----------------------USE TO RUN LOCALLY (DELETE CLASS FIXTURE AS WELL)(import UiAutomator2Options)-------------
android_caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:udid": "RF8M21KVM1K",
    # "appium:udid": "emulator-5554",
    "appium:platformVersion": "12",
    #"appium:platformVersion": "16",
    "appium:deviceName": "Galaxy S10",
    "appium:appPackage": "com.ibidev.ibitrade",
    "appium:appActivity": "com.ibidev.ibitrade.MainActivity",
    # Quality-of-life:
    "appium:autoGrantPermissions": True,
    "appium:newCommandTimeout": 120,
    # "appium:noReset": True, # Keep app state between runs
}
ios_caps = {
    "platformName": "iOS",
    "appium:automationName": "XCUITest",
    "appium:udid": "auto",
    "appium:bundleId": "com.ibidev.ibitrade",
    "appium:noReset": True, # This tells Appium NOT to try to reinstall the app
    "appium:autoAcceptAlerts": True, # iOS equivalent of auto-granting permissions
    "appium:newCommandTimeout": 120,
    # Optional: Helps Appium find the specific WDA you signed in Xcode
    # "appium:xcodeOrgId": "YOUR_10_DIGIT_TEAM_ID",
    # "appium:xcodeSigningId": "iPhone Developer"
}

@pytest.fixture(scope="function")
def set_web_driver(request):
    if platform == "android":
        opts = UiAutomator2Options().load_capabilities(android_caps)
    else:
        opts = XCUITestOptions().load_capabilities(ios_caps)

    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=opts)

    yield driver
    driver.quit()
