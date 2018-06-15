# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymssql


class ElongPipeline(object):
    def __init__(self):
        self.conn = pymssql.connect(host='111.230.108.124:10433', user='user_spider', password='spider911#', database='HotelSpider')
        self.cur = self.conn.cursor()
    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()
    def process_item(self, item, spider):

        item["Roomtotal"] = ''
        # 对城市进行清洗
        # if item["City"] == "香港" or item["City"] == "台湾":
        #     item["City"] = item["City"] + "市"
        # 对酒店等级进行清洗
        if str(item["Level"]) == "-14" or str(item["Level"]) == "14":
            item["Level"] = "高档公寓"
        elif str(item["Level"]) == "-4" or str(item["Level"]) == "4":
            item["Level"] = "高档型"
        elif str(item["Level"]) == "-3" or str(item["Level"]) == "3":
            item["Level"] = "舒适型"
        elif str(item["Level"]) == "-15" or str(item["Level"]) == "15":
            item["Level"] = "豪华公寓"
        elif str(item["Level"]) == "2" or str(item["Level"]) == "-2":
            item["Level"] = "经济型"
        elif str(item["Level"]) == "12" or str(item["Level"]) == "-12":
            item["Level"] = "经济公寓"
        elif str(item["Level"]) == "5" or str(item["Level"]) == "-5":
            item["Level"] = "豪华型"
        elif str(item["Level"]) == "-13" or str(item["Level"]) == "13":
            item["Level"] = "舒适公寓"
        # 对住房人数进行清洗

        if len(str(item["Room"]["People"])) > 1:
            item["Room"]["People"] = item["Room"]["People"][0]
        # 对酒店详情进行清洗 Description
        item["Description"] = item["Description"].replace(' ','').replace('\n','').replace("'",'')

        # 对酒店名字进行清洗 Hname
        item["Hname"] = item["Hname"].replace("’",'').replace("'",'')
        # 对酒店入住人数进行清洗 people
        if item["Room"]["People"] == "一":
            item["Room"]["People"] = 1
        elif item["Room"]["People"] == "二":
            item["Room"]["People"] = 2
        elif item["Room"]["People"] == "四":
            item["Room"]["People"] = 4
        elif item["Room"]["People"] == "六":
            item["Room"]["People"] = 6

        try:
            int(item["Room"]["People"])
        except Exception as e:
            print(item["Room"]["People"])
            item["Room"]["People"] = 2
        # 操作数据库
        self.unite_sql_hotel(item)
        self.unite_sql_room(item)
        self.unite_sql_price(item)
        self.insert_image(item)
        return item

    def insert_hotel(self,item):
        insert = "INSERT INTO Hotel (Source, HId, City, Name, Cover, [Level], Score, Address, Price, Phone, KYDate," \
                 + "RoomCount, ZXDate, Latitude, Longitude, Url, Description) values ('%d','%s','%s','%s','%s','%s','%f','%s','%.2f','%s','%s','%s','%s','%f','%f','%s','%s')" % (
            int((item["Source"])), str(item["HId"]), str(item["City"]), str(item["Hname"]), str(item["Cover"]),
            str(item["Level"]), float(item["Score"]), str(item["Address"]), float(item["index_price"]),
            str(item["HTel"]), str(item["KYdate"]), \
            str(item["Roomtotal"]), str(item["KYdate"]), float(item["Latitude"]), float(item["Longitude"]),
            str(item["Url"]), str(item["Description"])
        )
        try:
            self.cur.execute(insert)
            print("插入成功Hotel")
            self.conn.commit()
        except Exception as e:
            # print("插入失败Hotel")
            self.update_hotel(item)

    def update_hotel(self,item):

        update = "update Hotel set Score='%f',Price='%.2f',Phone='%s',ZXDate='%s',RoomCount='%s',UpdateTime='%s' where HId='%s'" %(
            float(str(item["Score"])),float(item["index_price"]),str(item["HTel"]),str(item["ZXdate"]),str(item["Roomtotal"]),str(datetime.datetime.now())[:23],str(item["HId"])
        )
        try:
            self.cur.execute(update)
            # print("更新成功Hotel")
            self.conn.commit()
        except Exception as e:
            print("更新失败Hotel")
            print(e)

    def insert_room(self, item):
        try:
            int(item["Room"]["People"])
        except Exception as e:
            print("*"*20)
            print("看看到底哪里错了 --%s"%item["Room"]["People"])

        insert = "INSERT INTO Room (Source, HId, RId, Cover, Name, Floor, Area, Price, People, Bed) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f','%d','%s')" % (
            int((item["Source"])), str(item["HId"]), str(item["Room"]["RId"]), str(item["Room"]["Cover"]),
            str(item["Room"]["Rname"]),
            str(item["Room"]["floor"]), str(item["Room"]["Rarea"]), float(item["Room"]["price"]),
            int(item["Room"]["People"]), str(item["Room"]["Rbed"])
        )

        try:
            self.cur.execute(insert)
            # print("插入成功Room")
        except Exception as e:
            # print("插入失败Room")
            self.update_room(item)
        self.conn.commit()

    def update_room(self,item):
        update = "update Room set Cover='%s',Name='%s',Price='%.2f',UpdateTime='%s' where RId='%s'" %(str(item["Room"]["Cover"]),str(item["Room"]["Rname"]),float(item["Room"]["price"]),str(datetime.datetime.now())[:23],str(item["Room"]["RId"]))
        try:
            self.cur.execute(update)
            # print("更新成功Room")
            # self.conn.commit()
        except Exception as e:
            print("更新失败Room")
            print(e)

    def insert_price(self,item):

        insert = "INSERT INTO Price (Source, HId, RId, PId, Name, Meal, [Rule], Price) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f')" %(
            int((item["Source"])),str(item["HId"]),str(item["Room"]["RId"]),str(item["Room"]["Ptype"]["PId"]),str(item["Room"]["Ptype"]["Pname"]),str(item["Room"]["Ptype"]["breakfast"]), item["Room"]["Ptype"]["rule"] ,float(item["Room"]["Ptype"]["price"])
        )

        try:
            self.cur.execute(insert)
            # print("插入成功Price")
        except Exception as e:
            # print("插入失败Price")
            # print(e)
            self.update_price(item)
        self.conn.commit()

    def update_price(self,item):
        update = "update Price set Name='%s',Price='%.2f',UpdateTime='%s' where PId='%s'" %(str(item["Room"]["Ptype"]["Pname"]),float(item["Room"]["Ptype"]["price"]),str(datetime.datetime.now())[:23],str(item["Room"]["Ptype"]["PId"]))
        try:
            self.cur.execute(update)
            # print("更新成功Price")
            # self.conn.commit()
        except Exception as e:
            print("更新失败Price")
            print(e)
            # self.conn.rollback()

    def insert_image(self,item):

        insert = "INSERT INTO Image (HId, RId, Url) VALUES"

        for image in item["Room"]["images"]:
            insert += "('%s','%s','%s')" %(str(item["HId"]), str(item["Room"]["RId"]),str(image))

        insert = insert.replace(")(","),(")
        try:
            self.cur.execute(insert)
            # print("插入成功Image")
        except Exception as e:
            # print(e)
            # print("插入失败Image")
            pass
        self.conn.commit()

    def unite_sql_hotel(self,item):
        sql = "if exists(select top 1 * from HotelSpider.dbo.Hotel where HId = '%s')" %str(item["HId"]) + \
              " begin update Hotel set Score='%f',Price='%.2f',Phone='%s',ZXDate='%s',RoomCount='%s',UpdateTime='%s' where HId='%s' end" %(
            float(str(item["Score"])),float(item["index_price"]),str(item["HTel"]),str(item["ZXdate"]),str(item["Roomtotal"]),
            str(datetime.datetime.now())[:23],str(item["HId"]))+ \
              " else begin INSERT INTO Hotel (Source, HId, City, Name, Cover, [Level], Score, Address, Price, Phone, KYDate," \
                 + "RoomCount, ZXDate, Latitude, Longitude, Url, Description) values ('%d','%s','%s','%s','%s','%s','%f','%s','%.2f','%s','%s','%s','%s','%f','%f','%s','%s') end" % (
            int((item["Source"])), str(item["HId"]), str(item["City"]), str(item["Hname"]), str(item["Cover"]),
            str(item["Level"]), float(item["Score"]), str(item["Address"]), float(item["index_price"]),
            str(item["HTel"]), str(item["KYdate"]), \
            str(item["Roomtotal"]), str(item["KYdate"]), float(item["Latitude"]), float(item["Longitude"]),
            str(item["Url"]), str(item["Description"])
        )
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("执行失败hotel")
            print(e)
            print(item)
        self.conn.commit()


    def unite_sql_room(self,item):
        sql = "if exists(select top 1 * from HotelSpider.dbo.Room where RId = '%s')" % str(item["Room"]["RId"]) + \
              " begin update Room set Cover='%s',Name='%s',Price='%.2f',UpdateTime='%s' where RId='%s' end" %(str(item["Room"]["Cover"]),str(item["Room"]["Rname"]),float(item["Room"]["price"]),str(datetime.datetime.now())[:23],str(item["Room"]["RId"]))+ \
              " else begin INSERT INTO Room (Source, HId, RId, Cover, Name, Floor, Area, Price, People, Bed) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f','%d','%s') end" % (
            int((item["Source"])), str(item["HId"]), str(item["Room"]["RId"]), str(item["Room"]["Cover"]),
            str(item["Room"]["Rname"]),
            str(item["Room"]["floor"]), str(item["Room"]["Rarea"]), float(item["Room"]["price"]),
            int(item["Room"]["People"]), str(item["Room"]["Rbed"])
        )
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("执行失败room")
            print(e)
            print(item)
        self.conn.commit()

    def unite_sql_price(self,item):
        sql = "if exists(select top 1 * from HotelSpider.dbo.Price where PId = '%s')" %str(item["Room"]["Ptype"]["PId"]) + \
              " begin update Price set Name='%s',Price='%.2f',UpdateTime='%s' where PId='%s' end" %(str(item["Room"]["Ptype"]["Pname"]),float(item["Room"]["Ptype"]["price"]),str(datetime.datetime.now())[:23],str(item["Room"]["Ptype"]["PId"]))+ \
              " else begin INSERT INTO Price (Source, HId, RId, PId, Name, Meal, [Rule], Price) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f') end" %(
            int((item["Source"])),str(item["HId"]),str(item["Room"]["RId"]),str(item["Room"]["Ptype"]["PId"]),str(item["Room"]["Ptype"]["Pname"]),str(item["Room"]["Ptype"]["breakfast"]), item["Room"]["Ptype"]["rule"] ,float(item["Room"]["Ptype"]["price"])
        )

        try:
            self.cur.execute(sql)
        except Exception as e:
            print("执行失败price")
            print(e)
            print(item)
        self.conn.commit()

