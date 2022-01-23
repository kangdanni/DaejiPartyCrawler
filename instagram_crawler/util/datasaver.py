import os
import json
import datetime
from instagram_crawler.util.settings import Settings
from instagram_crawler.util.util import check_folder


class Datasaver:
    def save_profile_json(username, information):
        check_folder(Settings.profile_location)
        if (Settings.profile_file_with_timestamp):
            file_profile = os.path.join(Settings.profile_location, username + '_' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H-%M-%S") + '.json')
        else:
            file_profile = os.path.join(Settings.profile_location, username + '.json')

        with open(file_profile, 'w') as fp:
            fp.write(json.dumps(information.to_dict(), indent=4))

    def save_profile_commenters_txt(username, user_commented_list):
        check_folder(Settings.profile_commentors_location)
        if (Settings.profile_commentors_file_with_timestamp):
            file_commenters = os.path.join(Settings.profile_commentors_location,
                                           username + "_commenters_" + datetime.datetime.now().strftime(
                                               "%Y-%m-%d %H-%M-%S") + ".txt")
        else:
            file_commenters = os.path.join(Settings.profile_commentors_location, username + "_commenters.txt")

        with open(file_commenters, 'w') as fc:
            for line in user_commented_list:
                fc.write(line)
                fc.write("\n")
        fc.close()

    def save_restaurant_keywords_txt(restaurant_keywords):
        check_folder(Settings.restaurant_keywords_location)
        if (Settings.restaurant_keywords_file_with_timestamp):
            restaurant_keywords_file = os.path.join(Settings.restaurant_keywords_location,
                                           "restaurant_keywords_" + datetime.datetime.now().strftime(
                                               "%Y-%m-%d %H-%M-%S") + ".txt")
        else:
            restaurant_keywords_file = os.path.join(Settings.restaurant_keywords_location, "restaurant_keywords.txt")

        with open(restaurant_keywords_file, 'w') as fc:
            for line in restaurant_keywords:
                fc.write(line)
                fc.write("\n")
        fc.close()