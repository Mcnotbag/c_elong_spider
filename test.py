import datetime
import json
import re

import requests

headers = {
    "Referer":"http://m.elong.com/hotel/?city=2003&indate=2018-05-31&outdate=2018-06-01",
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}
#
#
# response = requests.get("http://m.elong.com/hotel/91312077/",headers=headers)
#
# address = re.findall(r'<div class="addr">(.*?)</div>',response.content.decode())
# phone = re.findall(r"hotelTel : '(.*?)'",response.content.decode())
# Description = re.findall(r'"featureInfo":"(.*?)"',response.content.decode())
# Facilities = re.findall(r'"generalAmenities":"(.*?)"',response.content.decode())
# city = re.findall(r'province=;city=(.*?);',response.content.decode())[0]
# city = city[:-1]
# KYdate = re.findall(r'<dd>酒店开业时间 (.*?)年 </dd>',response.content.decode())
#
# print(KYdate)

# print(address)
# print(phone)
# print(Description)
# print(Facilities)

# addinfo = [{"key":"area","desp":"房间面积","content":"20平米"},{"key":"bed","desp":"床型","content":"大床1.5米"},
#            {"key":"network","desp":"上网方式","content":"免费无线"},{"key":"floor","desp":"楼层","content":"2-6层(普通楼层)"},
#            {"key":"personnum","desp":"可入住人数","content":"可入住2人"},
#            {"key":"psnnum","desp":"可入住人数","content":"2"},
#            {"key":"breakfast","desp":"早餐","content":"双早"},
#            {"key":"other","desp":"其他信息","content":"周租预定须知：被单更换：一周两次；保洁一天一次；水电物业费全包"}
#            ]
# if "breakfast" in str(addinfo):
#     print(str(addinfo))
#     breakfast = re.findall(r"{'key': 'bed', 'desp': '床型', 'content': '(.*?)'}",str(addinfo))[0]
#     print(breakfast)



# hotel_list_url = 'http://m.elong.com/hotel/api/list?_rt=1527472905302&indate={Indate}&t=1527472904279&outdate={Outdate}&city={cityId}&pageindex=0&actionName=h5%3D%3Ebrand%3D%3EgetHotelList&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=9168910'.format(Indate=datetime.date.today(), Outdate=datetime.date.today() + datetime.timedelta(days=1), cityId=2003)
#
# print(hotel_list_url)
# item = {}
# response = requests.get("http://m.elong.com/hotel/api/hoteldetailroomlist?_rt=1527736085429&hotelid=91063781&indate=2018-05-31&outdate=2018-06-01&actionName=h5%3D%3Ebrand%3D%3EgetHotelDetail&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=6873096",headers=headers)
#
# html_json = json.loads(response.content.decode())
#
# facili = html_json["recRoomInfo"]["recRpList"][0]["additionInfoList"]
# for i in facili:
#     print(i)
#     if "floor" in str(i):
#         item["floor"] = i.get("content")
#     if "personnum" in str(i):
#         item["people"] = i.get("content")
#
#

