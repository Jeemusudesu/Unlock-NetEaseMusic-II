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

    logging.info("Load Chrome extension NetEaseMusicWorld++")
    try:
        chrome_options.add_extension('NetEaseMusicWorld++.crx')
        logging.info("Extension added successfully!")
    except Exception as e:
        logging.error(f"Failed to added extension NetEaseMusicWorld++")
        logging.error(e)

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
    browser.add_cookie({"name": "MUSIC_U", "value": "006B191706435A1228D17B5C36DBC34203FF121A99F4F0F0F0CEEEF6AA7DE752186269198C1F8D5A8D4005DAA06F25F38CB5D7FE08AFA559E6315303B8EE6466B4067282B70A700CBF08609C249B6B1DEA8247390E3AFC47907A5BAAF0B8875BEC93808A486C355AEBE186F0A65EB71EDB2A8CD4ABBDBAA9D8E72C7E52B0AB6EE0150030A142A9A438E58F036DA7FB6A3BBA05916A4EDA990DA98107EED4502428515F3D4A31E9FCE7277D99D27C6969E01C0719CBAE97FAFFD82B09EF8E01CEF8E0D936D43EA5DC46F552E4CFDEE559B9E699A76FA3F5AEAE25722A3F521D514824693474DEBA5D4503681E5DF1811AE24D94F8C2729D503C4FAB02D733F0448F2F479CA012A2C4DE4B914EA4C25FC91AD17A5B87F924A509E1C223999AE308607B360BAD8E85B49A4ACF81ABAF0258865231AD57350CE17F9BAC7633AD85D7ED416A4DA65BCCA6A2EB1FAE8C8F511535341A965CA64E9B0470887ED5A2CF665C"})
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
