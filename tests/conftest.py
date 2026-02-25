import os

import dotenv
import pytest
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from api_client_v2.src.api.auth_api import AuthAPI

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
    #"appium:udid": "emulator-5554",
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


@pytest.fixture(scope="session")
def set_web_driver(appium_server, request):
    if platform == "android":
        opts = UiAutomator2Options().load_capabilities(android_caps)
    else:
        opts = XCUITestOptions().load_capabilities(ios_caps)

    # NOTE: appium_server fixture make sure we have appium client instance running
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=opts)

    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def appium_server():
    print("Starting Appium Server...")
    service = AppiumService()
    service.start(args=["--address", "127.0.0.1", "--port", "4723"]) # Args

    if not service.is_running or not service.is_listening: # Check if running
        raise Exception("Failed to start Appium Server!")

    print("✅ Appium Server Running!")

    yield service
    print("Stopping Appium Server...")
    service.stop()


@pytest.fixture(scope="session")
def api_client():
    """
    Returns an Authenticated API Client.
    Runs once per test session to save time.
    """
    client = AuthAPI()

    # Get credentials from .env
    user = os.getenv("API_USER")
    pwd = os.getenv("API_PASSWORD")

    # Perform the login flow
    client.login_and_get_tokens(user, pwd)

    return client