from instagram_crawler.crawl_profile_with_login import extract_choizaroad_location_names
from kakao_local_api.kakao_restaurant_info_scraper import get_restaurant_info
from kakao_map_crawler.util.chromedriver import SetupBrowserEnvironment
from kakao_map_crawler.util.extractor import extract_review_info


with SetupBrowserEnvironment() as browser:
    location_names = extract_choizaroad_location_names()
    print('location_names:', location_names)

    res = []
    for location_name in location_names:
        restaurant_info = get_restaurant_info(location_name)
        print('restaurant_info:', restaurant_info)
        if len(restaurant_info)>0 :
            reviews = extract_review_info(browser, restaurant_id=restaurant_info['id'])
            print('reviews:', reviews)
            res.append({'restaurant_info': restaurant_info, 'review': reviews})

    print(res)
