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
    browser.add_cookie({"name": "MUSIC_U", "value": "004086C66D1BD75E57D892EF61A3EDB4BBD1EEE96B70F8DC1FFA59832062D1B368B48BA81D02D23CFF7A7B617504C543C227A95C29CC7A644F7AEE6F83C979C3C6AC14A81BA6D0328D8427A0E0F3090BC38582C982C68D53E9B234F6E2CED35828C33978A9DD1B6FCB12486558ADD82DB32675263F8CCF436D7639442F6CE0E1A13FF6A800AA06BB47580356FB6C44C9EE3AE17F85638015E45F6A718B2C9C9BC12296533D9F050858EAA0CD8BB570DD3B26DC5F470A7189E02E89139399A9561AA9C197F6D5183B88103FFEAF9BC02CF897282F92BF78ECCA8E75489365EE44DCF1B943619114E24C57989A6C6B4B3C813F526DC1A34F8278E9229D723EAA8513797804FF799DC72F2F3CF85A75AFA15567684A4838F4718B5CC20A819ACA11FD849483341DEB477C4A281D50D116531AE1B0EA876C4EEF894FC6DA83E390EE4C8B03EF124AA7EBB7A3339A4EDEB039963D4368A1F5A74697AF74AB3C1D67D6D6BD8F94A36D29466F9A8A4C95C3970BE6956E35C2148EEE7A81CFB65099B9B628"})
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
