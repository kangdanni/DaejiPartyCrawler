import requests
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv


BASE_DIR = abspath(dirname(__file__))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
REST_API_KEY = getenv("REST_API_KEY", "")


def get_restaurant_info(keyword):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {"Authorization": f'KakaoAK {REST_API_KEY}'}
    params = {"query": keyword, "category_group_code": "FD6"} # FD6 => 음식점 코드
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"errorType: {response.json()['errorType']}] - message: {response.json()['message']}")
        return response.json()
    data = response.json()
    return data['documents'][0] if len(data['documents']) > 0 else {}


# print(get_restaurant_info('이원화구포국시'))
# print(get_restaurant_info(''))