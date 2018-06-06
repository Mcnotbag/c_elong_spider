import json
import re

import requests
from redis import Redis

# redis_server = Redis(host="111.230.34.217",port=6379,decode_responses=True)
#
# response = requests.get("http://m.elong.com/hotel/api/getlistfilter?_rt=1527502104816&cityid=2003")
# html_json = json.loads(response.content.decode())
# hot_city_list = html_json["hotCityList"]
# hot_city_list = eval(hot_city_list)
# for hot_city in hot_city_list:
#     need_city_list = {}
#     need_city_list[hot_city["cityName"]] = hot_city["cityId"]
#     print(need_city_list)
#     redis_server.lpush("elong_city",need_city_list)

# city = redis_server.mget("elong_hot_city")
# citys = redis_server.lpop("elong_hot_city")
# print(citys)
# print(type(citys))
# cityid = re.findall(r": '(\d+)'}",citys)
# print(cityid)

