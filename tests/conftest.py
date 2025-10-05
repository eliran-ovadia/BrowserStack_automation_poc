import pytest
from appium import webdriver
import dotenv
from appium.options.android import UiAutomator2Options

dotenv.load_dotenv()

# @pytest.fixture(scope='function')
# def set_web_driver(request, session_capabilities):
#     remoteURL = "https://hub.browserstack.com/wd/hub"
#     driver = webdriver.Remote(remoteURL, session_capabilities)
#     request.instance.driver = driver
#     request.node._driver = driver
#     yield driver
#     driver.quit()



# ----------------------USE TO RUN LOCALLY (DELETE CLASS FIXTURE AS WELL)(import UiAutomator2Options)-------------
local_caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:udid": "RF8M21KVM1K",
    "appium:platformVersion": "12",
    "appium:deviceName": "Galaxy S10",
    "appium:appPackage": "com.ibidev.ibitrade",
    "appium:appActivity": "com.ibidev.ibitrade.MainActivity",
    # Quality-of-life:
    "appium:autoGrantPermissions": True,
    "appium:newCommandTimeout": 120,
    #"appium:noReset": True, # Keep app state between runs
}
@pytest.fixture(scope="function")
def set_web_driver(request):
    opts = UiAutomator2Options().load_capabilities(local_caps)
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=opts)

    yield driver
    driver.quit()

