#!/usr/bin/env python3.5
"""Goes through all usernames and collects their information"""
import sys
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv
from instagram_crawler.util.settings import Settings
from instagram_crawler.util.datasaver import Datasaver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options as Firefox_Options

from instagram_crawler.util.cli_helper import get_all_user_names
from instagram_crawler.util.extractor import extract_information
from instagram_crawler.util.account import login
from instagram_crawler.util.chromedriver import init_chromedriver


chrome_options = Options()
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
chromeOptions.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--lang=en-US')
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})

capabilities = DesiredCapabilities.CHROME


try:
    browser = init_chromedriver(chrome_options, capabilities)
except Exception as exc:
    print(exc)
    sys.exit()


BASE_DIR = abspath(dirname(__file__))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
IG_USERNAME = getenv("IG_USERNAME", "")
IG_PASSWORD = getenv("IG_PASSWORD", "")

Settings.login_username = IG_USERNAME
Settings.login_password = IG_PASSWORD


def extract_choizaroad_location_names():
    try:
        usernames = ['choizaroad_official']
        for username in usernames:
            print('Extracting information from ' + username)
            information = []
            try:
                if len(Settings.login_username) != 0:
                    login(browser, Settings.login_username, Settings.login_password)
                information, user_commented_list = extract_information(browser, username, Settings.limit_amount)
                locations = [post['location'] for post in information.to_dict()['posts'] if post['location']]
                location_names = [location['location_name'] for location in locations]
                return location_names

            except Exception as e:
                print("Error with user " + username)
                print("Error trace:")
                print(e)
                sys.exit(1)


    except KeyboardInterrupt:
        print('Aborted...')

    finally:
        browser.delete_all_cookies()
        browser.close()


# location_names = extract_choizaroad_location_names()
# print(location_names)