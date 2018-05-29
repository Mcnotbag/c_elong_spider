# -*- coding: utf-8 -*-
import datetime
import json
import re
from pprint import pprint

import requests
import scrapy
from copy import deepcopy

from redis import Redis


class ElSpider(scrapy.Spider):
    name = 'EL'
    allowed_domains = ['elong.com']
    start_urls = ['http://m.elong.com/hotel']
    cur_cityid = None
    def parse(self, response):
        self.cur_cityid = self.get_city()
        hotel_list_url = 'http://m.elong.com/hotel/api/list?_rt=1527472905302&indate={Indate}&t=1527472904279&outdate={Outdate}&city={cityId}&pageindex=0&actionName=h5%3D%3Ebrand%3D%3EgetHotelList&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=9168910'.format(Indate=datetime.date.today(),Outdate=datetime.date.today() + datetime.timedelta(days=1),cityId=self.cur_cityid)
        yield scrapy.Request(
            hotel_list_url,
            callback=self.parse_list
        )

    def parse_list(self,response):
        html_str = response.body.decode()
        html_json = json.loads(html_str)
        try:
            hotels_list = html_json["hotelList"]
            page_str = html_json["hotelListUrlParameter"]["pageindex"]
        except Exception as e:
            print(e)
            with open("list_error.html","w",encoding="utf-8") as f:
                f.write(html_str)
        else:
            for hotel in hotels_list:
                item = {}
                item["Source"] = "3"
                item["Latitude"] = hotel["baiduLatitude"]
                item["Longitude"] = hotel["baiduLongitude"]
                item["Score"] = hotel["commentScore"]
                item["Url"] = hotel["detailPageUrl"]
                item["Hname"] = hotel["hotelName"]
                item["index_price"] = hotel["lowestPrice"]
                item["Cover"] = hotel["picUrl"]
                item["Level"] = hotel["starLevel"]
                item["HId"] = re.findall(r'http://m.elong.com/hotel/(\d+)/',item["Url"])[0]
                # 请求页面上的一些数据
                headers_hotel = {
                    "Referer": "http://m.elong.com/hotel/?city=2003&indate=2018-05-28&outdate=2018-05-29",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
                }
                other_url = "http://m.elong.com/hotel/{HId}/".format(HId=item["HId"])
                response_other = requests.get(other_url,headers=headers_hotel)
                item["Address"] = re.findall(r'<div class="addr">(.*?)</div>',response_other.content.decode())[0]
                item["HTel"] = re.findall(r"hotelTel : '(.*?)'",response_other.content.decode())[0]
                item["Description"] = re.findall(r'"featureInfo":"(.*?)"',response_other.content.decode())[0]
                item["Facilities"] = re.findall(r'"generalAmenities":"(.*?)"',response_other.content.decode())[0]
                item["City"] = re.findall(r'province=;city=(.*?);',response_other.content.decode())[0]
                item["KYdate"] = re.findall(r'<dd>酒店开业时间 (.*?)年 </dd>', response_other.content.decode())[0]
                item["ZXdate"] = item["KYdate"]
                # pprint(item)
                detail_hotel_url = "http://m.elong.com/hotel/api/hoteldetailroomlist?_rt=1527476977933&hotelid={HId}&indate={Indate}&outdate={Outdate}&actionName=h5%3D%3Ebrand%3D%3EgetHotelDetail&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=7556144".format(HId=item["HId"],Indate=datetime.date.today(),Outdate=datetime.date.today() + datetime.timedelta(days=1))
                yield scrapy.Request(
                    detail_hotel_url,
                    meta={"item":deepcopy(item),"dont_redirect":True},
                    callback=self.parse_detail,
                    errback=self.parse_error,
                    headers={
                        "Referer":other_url,
                        "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
                    }
                )
            # 翻页处理
            if not page_str:
                page_str = 0
            if len(hotels_list) == 20:
                print("*"*50)
                print("当前页的酒店数为--%d"%len(hotels_list))
                print("当前第---%s页"%(int(page_str)+1))
                print("*"*50)
                hotel_list_url = 'http://m.elong.com/hotel/api/list?_rt=1527472905302&indate={Indate}&t=1527472904279&outdate={Outdate}&city={cityId}&pageindex={page}&actionName=h5%3D%3Ebrand%3D%3EgetHotelList&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=9168910'.format(page=int(page_str)+1,Indate=datetime.date.today(),Outdate=datetime.date.today() + datetime.timedelta(days=1),cityId=self.cur_cityid)
                yield scrapy.Request(
                    hotel_list_url,
                    meta={"dont_redirect":True},
                    callback=self.parse_list,
                    errback=self.parse_error
                )
            # 翻页结束进行城市切换
            else:
                print("*"*50)
                print("当前页的酒店数为--%d" % len(hotels_list))
                print("当前城市Id---%s" %self.cur_cityid)
                self.cur_cityid = self.get_city()
                print("下个城市Id---%s" %self.cur_cityid)
                print("*"*50)
                hotel_list_url = 'http://m.elong.com/hotel/api/list?_rt=1527472905302&indate={Indate}&t=1527472904279&outdate={Outdate}&city={cityId}&pageindex=0&actionName=h5%3D%3Ebrand%3D%3EgetHotelList&ctripToken=&elongToken=dc8bc8aa-b5cb-4cc0-a09e-4291a67df718&esdnum=9168910'.format(
                    Indate=datetime.date.today(), Outdate=datetime.date.today() + datetime.timedelta(days=1),
                    cityId=self.cur_cityid)
                yield scrapy.Request(
                    hotel_list_url,
                    callback=self.parse_list
                )

    def parse_detail(self,response):
        item = response.meta["item"]
        html_str = response.body.decode()
        html_json = json.loads(html_str)
        room_list = html_json["roomInfoList"]
        for room in room_list:
            item["Room"] = {}
            item["Room"]["RId"] = room["roomId"]
            item["Room"]["RId"] = item["HId"] + item["Room"]["RId"]
            item["Room"]["Rname"] = room["roomInfoName"]
            item["Room"]["Rarea"] = room["area"]
            item["Room"]["Rbed"] = room["bed"]
            item["Room"]["Cover"] = room["coverImageUrl"]
            item["Room"]["images"] = room["imageList"]
            item["Room"]["price"] = room["minAveragePriceSubTotal"]
            # 一些必要的信息
            floor = str(room["rpList"][0]["additionInfoList"])
            item["Room"]["floor"] = re.findall(r"{'key': 'floor', 'desp': '楼层', 'content': '(.*?)'}",floor)[0] if "floor" in floor else ''
            item["Room"]["People"] = re.findall(r"{'key': 'personnum', 'desp': '可入住人数', 'content': '可入住(\d+)人'}",floor)[0] if "personnum" in floor else 0
            for rprice in room["rpList"]:
                item["Room"]["Ptype"] = {}
                addinfo = str(rprice["additionInfoList"])
                item["Room"]["Ptype"]["breakfast"] = re.findall(r"{'key': 'breakfast', 'desp': '早餐', 'content': '(.*?)'}",addinfo)[0] if "breakfast" in addinfo else '无'
                item["Room"]["Ptype"]["PId"] = rprice["ratePlanId"]
                item["Room"]["Ptype"]["PId"] = str(item["Room"]["RId"]) + str(item["Room"]["Ptype"]["PId"])
                item["Room"]["Ptype"]["rule"] = rprice["cancelTag"]
                item["Room"]["Ptype"]["price"] = rprice["averagePriceSubTotal"]
                item["Room"]["Ptype"]["Pname"] = rprice["productName"]
                item["Room"]["Ptype"]["Pname"] = item["Room"]["Rname"] + item["Room"]["Ptype"]["Pname"]

                yield deepcopy(item)

    def parse_error(self,error):
        print("没有请求成功,可能跳转了")

    def get_city(self):
        redis_server = Redis(host="111.230.34.217", port=6379, decode_responses=True)
        city_str = redis_server.rpop("elong_hot_city")
        print("*"*20)
        print(city_str)
        cityid = 2003
        if city_str:
            cityid = re.findall(r": '(\d+)'}", city_str)[0]

        return cityid