from sqlite3 import connect
import psycopg2 as pg2
import os
from os import getenv

DB_NAME = getenv("DB_NAME","")
DB_HOST =  getenv("DB_HOST","")
DB_USER =  getenv("DB_USER","")
DB_PASSWORD =  getenv("DB_PASSWORD","")
DB_PORT =  getenv("DB_PORT","")


def insert_restaurant_info(res):
  try :

    conn = pg2.connect(database =DB_NAME, user = DB_USER, password = DB_PASSWORD, host = DB_HOST, port = DB_PORT)

    cur = conn.cursor()

    place_info = dict()
    review= dict()

    #place insert
    place_info['id'] = res['restaurant_info']['id']
    place_info['category_name'] =  res['restaurant_info']['category_name']
    place_info['phone']=   res['restaurant_info']['phone']
    place_info['place_name'] =   res['restaurant_info']['place_name']
    place_info['place_url'] =  res['restaurant_info']['place_url']
    place_info['road_address_name'] = res['restaurant_info']['road_address_name']

    sql = '''
        INSERT INTO
                place
        VALUES ('{0}', '{1}','{2}','{3}','{4}','{5}')
      '''
    print(sql.format(*place_info.values()))

    cur.execute(sql.format(*place_info.values()))
    conn.commit()

    #review insert
    for j in res['reviews']:
      review['id'] = place_info['id']
      review['rating']= j['rating']
      review['commennt'] = j['comment']

      sql2 = '''
        INSERT INTO
                  review
        VALUES ('{0}', '{1}','{2}')
      '''

      print(sql2.format(*review.values()))

      cur.execute(sql2.format(*review.values()))
      conn.commit()



  except Exception as e :
    print (e)

  finally:
    if conn:
      conn.close()




test = dict()
test['restaurant_info'] =  {'address_name': '서울 마포구 상수동 321-1', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 중식 > 중화요리', 'distance': '', 'id': '19032013', 'phone': '02-322-2653', 'place_name': '맛이차이나', 'place_url': 'http://place.map.kakao.com/19032013', 'road_address_name': '서울 마포구 독막로 68', 'x': '126.920850347282', 'y': '37.5475849357353'}
test['reviews'] =  [{'rating': 4, 'comment': ''}, {'rating': 5, 'comment': '중국식 냉면 정말 맛있더라구요. '}, {'rating': 4, 'comment': '요리는 매우 좋은 편. 짜장의 경우 시간대에 따라 맛이 달라짐. 오픈 직후의 짜장이 가장 훌륭함. '}, {'rating': 4, 'comment': ''}, {'rating': 1, 'comment': '런치세트이 1인 가격 써놓고 2인 이상만 주문 받는 이상한 곳. 2인 이상만 된다고 써놓든가. 직원들도 불친절'}]

print(insert_restaurant_info(test))