from util.chromedriver import SetupBrowserEnvironment
from util.extractor import extract_review_info


def extract_restaurant_review(restaurant_id):
    with SetupBrowserEnvironment() as browser:
        restaurant_id = '1316757553' # 이원화구포국시 카카오맵ID
        reviews = extract_review_info(browser, restaurant_id=restaurant_id)
        print('reviews', reviews)