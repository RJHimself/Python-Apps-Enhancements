#!/usr/bin/env python3
#exe: py-chrome


import ast
import sys
import atexit


@atexit.register
def on_script_exit():
    if len(sys.argv) < 2: return

    def convert_values(value):
        #  This Function converts Numbers like "Int" or "Float" from "strings" coming from the terminal to the actual Types, like "Int" and "Float"

        try: value = ast.literal_eval(value)
        except: value=value
        return value


    args=""
    function_name=sys.argv[1]
    if len(sys.argv) > 2: args=list(map(convert_values, sys.argv[2:]))
    getattr(sys.modules[__name__], "%s" % function_name)(*args)


# WARNING:
# ALL of The Code above is what makes this Script able to be Called in a Terminal
# This type of python cli is at least possible with python 3.7.5 (64 bits)
# ------------------------------------------------------------------------


import time
from glob import glob
from os.path import expanduser

from selenium import webdriver
from selenium.webdriver import Chrome as Browser_Webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from python_enhancements import string

import importlib
ui = importlib.import_module("python_apps_enhancements.web.ui")


home = expanduser("~")
app_name="chromium"
app_location=home+"/.config/"+app_name


class Profile_Options(Options):
    def __init__(self, profile=None):
        Options.__init__(self)

        if profile:
            profile_number=string.extract.integers(str(profile))[0]
            profile="Profile {number}".format(number=profile_number)

            self.add_experimental_option(
            'excludeSwitches',
            ['disable-sync'])
            self.add_argument('--enable-sync')
            self.add_argument("profile-directory="+profile)


        self.add_argument("--user-data-dir="+app_location)

class Start(Browser_Webdriver):
    def __init__(self, as_user= None, profile=None, executable_path="/usr/bin/chromedriver"):
        options=Profile_Options(profile) if as_user else Options()
        Browser_Webdriver.__init__(self, executable_path=executable_path, options=options)


def login(email, password, profile=None):
    # Quiting due to Lack of Arguments
    if 'email' not in locals() or 'password' not in locals():
        print("Quiting due to Lack of Arguments"); return


    execute_macro([
        # Open login Page
        {"link": "https://accounts.google.com/signin/chrome/sync/identifier?ssp=1&continue=https%3A%2F%2Fwww.google.com&flowName=GlifDesktopChromeSync"},
        # Log In
        {"write": email, "enter": True, "element": "input[type='email'][id='identifierId']"},
        {"timeout": 3},
        {"write": password, "enter": True, "element": "input[type='password'][name='password']"},
        # Waiting for chrome to Load the New Account
        {"timeout": 5},
    ], profile=profile)


def login_by_google(browser=None, link=None, button=None, profile=None):
    # EXAMPLE
    # login_by_google(link="https://www.notion.so/login", button=".notion-login > [role='button']")


    if not browser and not link and not button: return print("Quiting due to Lack of Arguments ...")
    launch_browser=True if link and button else False
    if launch_browser:
        browser = Start(as_user=True, profile=profile)
        browser.get(link)

        ui.get_element(browser, button).click()


    url_to_find="accounts.google.com/signin/oauth/oauthchooseaccount?"
    window_main=browser.window_handles[0]

    # Giving Time for New windows to Load
    time.sleep(3)


    for window in browser.window_handles:
        browser.switch_to.window(window)

        for i in range(2):
            time.sleep(3)
            if url_to_find in browser.current_url:
                # Email Account Button
                ui.get_element(browser, "[data-identifier]:nth-of-type(1)").click()
                break
            pass


    browser.switch_to.window(window_main)


    # Waiting for chrome to Load the New Account
    time.sleep(5)
    if launch_browser: browser.quit()


def sync(email, password, profile=list_profiles()[0]):
    # Quiting due to Lack of Arguments
    if 'email' not in locals() or 'password' not in locals():
        print("Quiting due to Lack of Arguments"); return


    login(email, password, profile=profile)

    buttons_location="document.querySelector('settings-ui:nth-of-type(1)').shadowRoot.querySelector('settings-main:nth-of-type(1)').shadowRoot.querySelector('settings-basic-page[role=\"main\"]').shadowRoot.querySelector('settings-people-page:nth-of-type(1)').shadowRoot.querySelector('settings-sync-page:nth-of-type(1)').shadowRoot.querySelector('settings-sync-account-control:nth-of-type(1)').shadowRoot"

    execute_macro([
        # Open login Page
        {"link": "chrome://settings/syncSetup"},
        # Log In
        {"lang": "js", "click": buttons_location+".querySelector('#sync-button')"},
        {"timeout": 3},
        {"lang": "js", "click": buttons_location+".querySelector('#setup-buttons > .action-button[role=\"button\"]')"},
        # Waiting for chrome to Load the New Account
        {"timeout": 5},
    ], profile=profile)


def list_profiles():
    profiles_locations=[]
    profiles_list=[]


    for directory in glob(app_location+"/*/"):
        if app_location+"/Profile " in directory:
            profiles_locations.append(directory)

    for profile in profiles_locations:
        profiles_list.append(string.extract.integers(profile)[0])


    return profiles_list


def execute_macro(macro, browser=None, profile=None):
    # Prevention for any possible Unclosed Browser
    time.sleep(3)

    launch_browser = False if browser else True
    if launch_browser:
        options=Profile_Options(list_profiles()[0])
        browser = Start(as_user=True, profile=profile)


    for command in macro:
        if not command.get("lang"): command["lang"]="css"


        if "link" in command:
            browser.get(str(command.get("link").strip()))
        elif "timeout" in command:
            time.sleep(command.get("timeout"))
        elif "click" in command:
            ui.get_element(browser, str(command.get("click")), lang=str(command.get("lang"))).click()
        elif "write" in command:
            element=ui.get_element(browser, str(command.get("element")), lang=str(command.get("lang")))
            element.send_keys(command.get("write"))

            if command.get("enter"):
                element.send_keys(Keys.ENTER)


    # The Body it's Only being acquired to, cuz for some fucked up reason, chrome is not saving the last option, so we'l send 0 to the body at the End, and Every other setting will be saved except the body
    body=ui.get_element(browser, "body:nth-of-type(1)")
    body.send_keys("0")

    if launch_browser: browser.quit()
    time.sleep(5)
