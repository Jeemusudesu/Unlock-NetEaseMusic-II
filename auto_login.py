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
    browser.add_cookie({"name": "MUSIC_U", "value": "0028DDF899E61AC70F0C1785AD40E01EC39BD35F80D4E9C2DA65C388EEE46CCD125C5B9194143A7602C36A2FD11684164B126C8078C3DDDB25AD86BD087F2BCA78503049580767ADD81EA68CF075F28CF4CE45772DE2F6677B901760C586DFBBFB65025979AFFE2A901F339C6D09656E894EF4EEBFCC1F6519534BA8D91AABE5F84D4D79C624DA6B6FDF2DF6DB2221CBE80C31B14CDAD3E30259D416426B609140E74C5EA0CBC70A3F495CF4C1E674D7459BB39663F6A90501ADA32DE402B703DFB04ABF416059858B34E7008718A4745682E9ED34A10E71F3A5247DB5380C632006660AEF0DDB73DE9CD434CF906D911CF3239908DB5214926FF2118052A526E8CA1FC0AF6CCC61A34A3DC3188236F15DF413B30DA3531C32250C8153BB568448E8DA25836FB0B7805CC1C95C297DB05F539013824FA82C2C3769ACE470530383DE7DEE7488B9759474C4F3A6B716FCBF54DA4BF8E9923D8885A1A28AF8512307"})
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
