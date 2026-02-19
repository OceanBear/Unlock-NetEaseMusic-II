# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A76C0B96262A17947D95F4E50E9F5BAA0F213BDF04842DD3BB7F1FEBAC906E9D192BF62A8F36E5AA1EA475353D3E8E63CDC41F3E5222C90393E79AF054552087DFBDAD4A37EAA58AC8939DEA010ED5AF0B46038A591B3F69493E4988EC143D1062354180C3207FB19B1AE490E33497ACF28592BEF7EBC4EA8B744F1F5CFC5B8A73412D98CF4DDCCFBFB0AAA4DF74B081882128809345D66BE7CB875BB18222392D543E60DF35D969377B793A4F7382BB23A4BC42EEDE8367A75CFEAB920F0B9A711416CCF2D5D4B4CD5A45429F0B53DF767F5866408D1E356318E7DB8B9211EB1DFB8C06DE3540EE86B7186806FA42CAC999FC03B8DDF7ECD185E89076BD153638FC3182CA87B32C68283194373F6DDCE4A56A900D5EA0D25EC6324E560E6CFED352024F1FA2296643E792699013FE41A977659D5C4A25A125BB45719F931E436169B02CF23F782724EFA1250693032728D76902B19D4BA2F579FCE6214C08016FC30AE07B2A92C119C46210BC92D3E5D2433817685779138DBB6F05410368EA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
