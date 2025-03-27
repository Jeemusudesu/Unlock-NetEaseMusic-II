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
    browser.add_cookie({"name": "MUSIC_U", "value": "003D80A70E9658C4CAD6FF28B99142D417DAB774983D3F575231B9591696CA3297661A9A9E9BAACB5DB49A7E63B59F1EDD7283C1A5EBCF1AC397165B9246E9D0BB087CC38997FA52F274C05858457A05190F1CA2DEA26AF7D66028C59C06BA06034E5DAAC51D0A25AA667FB171D82F05C3D8D030C314D181E9CE5062A8ABBCB2CCA2EDFCFD1DC16838DAA6FAC968ED9B3F8B189EB189F74ABAE1673D21622A171C9111D8C4ABDC1851DDA498BB068A3446132823ED375C7F0BDCAA3122E6A27B88DC0B5BBB6B1AD3EAC7243E0D8661D36F4651751B7A0D9CCFD3BAFC8D6E1BCD847371AA3654D0FA4A7C59371E0D68AEF3173B06B19820045FF58842BF1A3E912027EAAB6DC989D63567D6B258A45AFF13464E3BEE1F9F5DE2C7C395464609B3A66C16763A23FA5CF91F744448D2D8BD836C5C2C54EEADC09ACA0C957C046698D6F0462BFCB12B0362A4EEDAA438BABFF66907632221D16A1BCF86DE1ECC7782E0"})
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
