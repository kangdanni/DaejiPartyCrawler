from time import sleep

from kakao_map_crawler.util.logger import KakaoMapCrawlingLogger
from kakao_map_crawler.util.util import web_adress_navigator
from kakao_map_crawler.util.exceptions import PageNotFound404, NoRestaurantPageFound

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


def extract_review_info(browser):
    main_article_section = browser.find_element_by_css_selector("#kakaoContent > #mArticle") 
    comment_section = main_article_section.find_element_by_css_selector("div[data-viewid='comment']")
    review_lists = comment_section.find_elements_by_css_selector(".list_evaluation > li")

    reviews = []
    for review_list in review_lists:
        review_id = review_list.get_attribute('data-id')
        rating_element = review_list.find_element_by_css_selector('.star_info .num_rate')
        comment_element = review_list.find_element_by_css_selector('.comment_info .txt_comment > span')
        if rating_element is not None and comment_element is not None:
            reviews.append({
                'id': review_id,
                'rating': int(rating_element.text),
                'comment': comment_element.text,
            })
    return reviews


def extract_reviews(browser, restaurant_id):
    try:
        restaurant_link = f"https://place.map.kakao.com/{restaurant_id}"
        web_adress_navigator(browser, restaurant_link)
        KakaoMapCrawlingLogger.logger().info(f"Extracting information from {restaurant_id}")
    except PageNotFound404 as e:
        raise NoRestaurantPageFound(e)

    reviews = []
    reviews.extend(extract_review_info(browser))

    try:
        page_count = len(browser.find_elements_by_class_name('link_page'))
        index = 3
        for i in range(page_count - 1):
            browser.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(index) +')').send_keys(Keys.ENTER)
            sleep(1)
            reviews.extend(extract_review_info(browser))
            index += 1
        browser.find_element_by_link_text('??????').send_keys(Keys.ENTER) # 5???????????? ?????? ?????? ?????? ?????? ?????????
        sleep(1)
        reviews.extend(extract_review_info(browser))
    except (NoSuchElementException, ElementNotInteractableException):
        print("no review in crawling")
    print('??? ????????? ???')

    # ??? ?????? ?????????
    while True:
        index = 4
        try:
            page_count = len(browser.find_elements_by_class_name('link_page'))
            for i in range(page_count - 1):
                browser.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(index) +')').send_keys(Keys.ENTER)
                sleep(1)
                reviews.extend(extract_review_info(browser))
                index += 1
            browser.find_element_by_link_text('??????').send_keys(Keys.ENTER) # 10????????? ???????????? ???????????? ?????? ?????? ?????? ??????
            sleep(1)
            reviews.extend(extract_review_info(browser))
        except (NoSuchElementException, ElementNotInteractableException):
            print("no review in crawling")
            break
    return [{**review, 'restaurant_id': int(restaurant_id)} for review in reviews]