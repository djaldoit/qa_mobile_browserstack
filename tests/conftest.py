import allure
import pytest
from appium.options.android import UiAutomator2Options
from selene import browser
import config
import os
from selene_in_action import utils
from appium import webdriver


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Configurate options'):
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "10.0",
            "deviceName": "Google Pixel 4",

            # Set URL of the application under test
            "app": "bs://sample.app",

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": config.bstack_userName,
                "accessKey": config.bstack_accessKey,
            }
        })

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.allure.attach_bstack_video(session_id)


