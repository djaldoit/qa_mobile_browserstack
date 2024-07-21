import allure
import requests
import os
from dotenv import load_dotenv


load_dotenv()
user_name = os.getenv("USERNAME")
access_key = os.getenv("ACCESS-KEY")


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, name='page_source', attachment_type=AttachmentType.XML)


def add_video(session_id):
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(user_name, access_key),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )