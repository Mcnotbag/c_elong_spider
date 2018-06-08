import json
import string

import requests
from redis import Redis

# redis_server = Redis(host="111.230.34.217",port=6379,decode_responses=True)
# # first_letter = string.ascii_uppercase
# first_letter = "STUVWXYZ"
# url = "http://m.elong.com/hotel/api/gethotelcitysbyletter?_rt=1527589494989&letter={id}"
#
# for i in first_letter:
#     url = "http://m.elong.com/hotel/api/gethotelcitysbyletter?_rt=1527589494989&letter={id}".format(id=i)
#     response = requests.get(url)
#     html_json = json.loads(response.content.decode())
#     for city in html_json:
#         need_city_list = {}
#         need_city_list[city["cityName"]] = city["cityId"]
#         print(need_city_list)
#         redis_server.lpush("elong_city", need_city_list)

