import json
import string
import csv
import requests
from redis import Redis

redis_server = Redis(host="111.230.34.217",port=6379,decode_responses=True)
first_letter = string.ascii_uppercase
url = "http://m.elong.com/hotel/api/gethotelcitysbyletter?_rt=1527589494989&letter={id}"

for i in first_letter:
    url = "http://m.elong.com/hotel/api/gethotelcitysbyletter?_rt=1527589494989&letter={id}".format(id=i)
    response = requests.get(url)
    html_json = json.loads(response.content.decode())
    for city in html_json:
        # 存入redis
        # need_city_list = {}
        # need_city_list[city["cityName"]] = city["cityId"]
        # print(need_city_list)
        # redis_server.lpush("elong_city", need_city_list)
        # 存入csv文件
        csv_need_city = [city["cityName"],city["cityId"]]

        with open("elong_all_city.csv","a",encoding="utf-8") as f:
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(csv_need_city)


