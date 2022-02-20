import psycopg2
from pprint import pprint
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv

from instagram_crawler.crawl_profile_with_login import extract_choizaroad_location_names
from kakao_local_api.kakao_restaurant_info_scraper import get_place_info
from kakao_map_crawler.util.chromedriver import SetupBrowserEnvironment
from kakao_map_crawler.util.extractor import extract_review_info
from utils.postgresql_manager import PostgresqlManager


postgresql_manager = PostgresqlManager()


with SetupBrowserEnvironment() as browser:
    location_names = extract_choizaroad_location_names(browser)
    print('location_names:', location_names)
    for location_name in location_names:
        try:
            place_info = get_place_info(location_name)
            postgresql_manager.insert_one(table_name='place', data=place_info)
            print(f'{place_info["place_name"]} data inserted!')

            reviews = extract_review_info(browser, restaurant_id=place_info['id'])
            postgresql_manager.insert_many(table_name='review', data=reviews)
            print(f'{place_info["place_name"]} review data inserted!')
        except Exception as e:
            print("Error with location " + location_name)
            print("Error trace:", e)
        