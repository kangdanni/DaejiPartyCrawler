import requests
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv

from requests.api import get


BASE_DIR = abspath(dirname(__file__))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
CLIENT_ID = getenv("CLIENT_ID", "")
CLIENT_SECRET = getenv("CLIENT_SECRET", "")


def get_restaurant_info(keyword):
    url = 'https://openapi.naver.com/v1/search/local.json'
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    params = {
        'query': keyword,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"errorCode: {response.json()['errorCode']} - errorMessage: {response.json()['errorMessage']}")
        return response.json()
    data = response.json()
    return data['items'][0] if len(data['items']) > 0 else {}


print(get_restaurant_info('이원화구포국시'))
# print(get_restaurant_info(''))
