from . import select

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element(browser, location, timeout=30, lang="css"):
    lang=lang.lower()

    try:
        if lang == "css":
            return WebDriverWait(browser, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, location))
            )
        if lang == "css-query":
            time.sleep(3)
            return browser.execute_script("return document.querySelector('"+location+"')")
        if lang == "js":
            time.sleep(3)
            return browser.execute_script("return "+location)
    except:
        print("An Exception Occurred")

    return
