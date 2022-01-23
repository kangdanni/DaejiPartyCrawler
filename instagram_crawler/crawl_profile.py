#!/usr/bin/env python3.5
"""Goes through all usernames and collects their information"""
import sys

from instagram_crawler.util.account import login
from instagram_crawler.util.chromedriver import SetupBrowserEnvironment
from instagram_crawler.util.cli_helper import get_all_user_names
from instagram_crawler.util.datasaver import Datasaver
from instagram_crawler.util.extractor import extract_information
from instagram_crawler.util.extractor_posts import InstagramPost
from instagram_crawler.util.settings import Settings


with SetupBrowserEnvironment() as browser:
    # usernames = get_all_user_names()
    usernames = ['choizaroad_official']
    for username in usernames:
        print('Extracting information from ' + username)

        information, user_commented_list = extract_information(browser, username, Settings.limit_amount)

        Datasaver.save_profile_json(username, information.to_dict())
        print ("Number of users who commented on their profile is ", len(user_commented_list),"\n")

        Datasaver.save_profile_commenters_txt(username, user_commented_list)
        print ("\nFinished. The json file and nicknames of users who commented were saved in profiles directory.\n")
