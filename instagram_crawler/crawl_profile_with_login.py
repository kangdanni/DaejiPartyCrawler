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


BASE_DIR = abspath(dirname(__file__))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
IG_USERNAME = getenv("IG_USERNAME", "")
IG_PASSWORD = getenv("IG_PASSWORD", "")

Settings.login_username = IG_USERNAME
Settings.login_password = IG_PASSWORD


def extract_choizaroad_location_names(browser):
    usernames = ['choiza11']
    for username in usernames:
        print('Extracting information from ' + username)
        information = []
        try:
            if len(Settings.login_username) != 0:
                login(browser, Settings.login_username, Settings.login_password)
            information, user_commented_list = extract_information(browser, username, Settings.limit_amount)
            locations = [post['location'] for post in information.to_dict()['posts'] if post['location']]
            location_names = [location['location_name'] for location in locations]
            location_names = list(set(location_names))
            return location_names

        except Exception as e:
            print("Error with user " + username)
            print("Error trace:", e)
