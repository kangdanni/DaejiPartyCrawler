import requests
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv


BASE_DIR = abspath(dirname(__file__))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
REST_API_KEY = getenv("REST_API_KEY", "")


def get_place_info(keyword):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {"Authorization": f'KakaoAK {REST_API_KEY}'}
    params = {"query": keyword, "category_group_code": "FD6"} # FD6 => 음식점 코드
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"errorType: {response.json()['errorType']}] - message: {response.json()['message']}")
        return response.json()
    data = response.json()
    place_info = data['documents'][0] if len(data['documents']) > 0 else {}
    place_info = {key: place_info[key] for key in 
        ['id', 'category_name', 'place_name', 'place_url', 'phone', 'road_address_name']}
    place_info['id'] = int(place_info['id'])
    return place_info
