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
    browser.add_cookie({"name": "MUSIC_U", "value": "001E439CA86295A08F0E9908912C97A7758AC3788192A1345DCD00B09D9E17A96C3B98C25AFDB85AD4232AC98B3F2EC70EC091289E3D8FDD764B81B486FDD7378137C951DAC1D82C1838673D61609F68EBFA9DBAC60E17342F8C3C1871EDD518E34B64D3097EA1BA51FDCB46D9CFFE2AFBCED7226EB9D1F5FFE9AE42CDE8D2F9EECFBB9B3B7189B085BCD8F55387B8D4318D6327FA1C5379DFB1DBA9DB65360B52152EF529A58D1302325C546B830878DE537347B858C52F5D3FFCCDB8E3F408993E267393BA5773C2A78142BB3BDDFE3B6F3853A75E6C810D454D3A9DA067C86120F5A668A7CE2FDA932AD5A0498476E17F74EA04344AF32EDF8C637D3E47CD6A00E830683FF97A7BB79E17B3C151D0D46539097F1037271AAC33BD49446A43D71D18E5132537C15F6E651291013D19C48528F99289DDA070C06A412F4283ACA07B4007961015272F3C2D1215FB4555C7A348D47ADE3E5817091D9A9A8556F40D49D8DED997ECE24734D4311C4C3FEB947140F3065D70596A927A66E2926477E7"})
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
