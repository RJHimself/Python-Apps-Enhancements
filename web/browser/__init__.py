from . import chrome

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def isNotOpen(browser): return not isOpen(browser)
def isOpen(browser):
    try:
        browser.title
        return True
    except WebDriverException:
        return False
