# -*- coding: UTF-8 -*-
'''
Created on 2019 10月 24日

@author: surface
'''

import requests
import time
from PyQt5.QtCore import QObject
from bs4 import BeautifulSoup
from urllib import parse


class URL(object):
    
    #query_url GET
#   https://m.quyundong.com/court/book?bid=22377&t=1572278400&cid=1
#     1. bid:22377
#     2. t:1572278400
#     3. cid:1
    query_ticket_url = "https://m.quyundong.com/court/book?"
    
    #confirm_order GET
# price[]:40
# hour[]:7
# course_name[]:A号场
# real_time[]:7:00-8:00
# allcourse_name:A号场,B号场,C号场,D号场,
# goods_ids:298108643
# book_date:1572278400
# court_name:上海市徐汇区青少年水上运动学校
# category_name:羽毛球
# bid:22377
# cid:1
# order_type:0
# relay:0
    confirm_order_url = "https://m.quyundong.com/order/Confirm?"
    
    
    #doorder GET
#     goods_ids:298108643
# act_id:0
# code:0
# bid:22377
# cid:1
# coupon_id:0
# ticket_type:1
# utm_source:
# pay_type:
# card_no:
# relay:0
# package_type:0
# hash:017c698ec6d7fc61a449e88eeceacc0b
# _:1571888420740

    doorder_url = "https://m.quyundong.com/order/doconfirm?"

    

class APITool(QObject):
    session = requests.session()
    
    serverid = "ea16ff80abbcfc187fe38174255bf06e|1573699730|1573699646"
    date_str = '2019-11-20'
    hr = 11
    
    cookies_info_dict = { 
                         "SERVERID":  serverid,   #need to be changed
                         "PHPSESSID":"joc48cr8kopr08p2cgdqujegt3",
                         #"wx_hash" : "234dc9f18382888227ec23f901864770",
                         "wx_nick_name" : "428819",
                         "wx_phone" :  "13764288196",
                         "wx_uid" : "Itnft4H4bj4Xye8bhSjI",
                         "wx_userToken":"f4%2BK5oSubzEXyeoVhyLDAIVrEA"
                         }
    
    badminton_info_dict = {
                        "bid":22377,
                        "t":  int (time.mktime( time.strptime( date_str,'%Y-%m-%d') )  ),
                        "cid":1
                      }
    
    order_dict = {
                "price[]":0,
                "hour[]": hr,
                "course_name[]":"",
                "real_time[]":"",
                "allcourse_name":"A号场,B号场,C号场,D号场",
                "goods_ids":0,
                "book_date":0,
                "court_name":"上海市徐汇区青少年水上运动学校",
                "category_name":"羽毛球",
                "bid":22377,
                "cid":1,
                "order_type":0,
                "relay":0

        }

    doconfirm_dict = {
                "goods_ids":"",
                "act_id":0,
                "code":0,
                "bid":22377,
                "cid":1,
                "coupon_id":0,
                "ticket_type":1,
                "utm_source":"",
                "pay_type":"",
                "card_no":"",
                "relay":0,
                "package_type":0,
                "hash":"",
                "_":0
        
        }
    

            
    
    @classmethod
    def query_ticket(cls):  
        print("Step: query_ticket (actually set tk in cookies...)")
        
        for key,value in APITool.cookies_info_dict.items():
            cls.session.cookies.set(key, value, domain="m.quyundong.com")
        print("cookies: ",cls.session.cookies)
        
        whole_query_ticket_url = URL.query_ticket_url + parse.urlencode( APITool.badminton_info_dict )
        print("query_url: ",whole_query_ticket_url)
        response = cls.session.get( whole_query_ticket_url )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        li_list = soup.find_all("li")
        for item in li_list:
            #print(str(item))
            #print("")
            hr = str(APITool.order_dict["hour[]"] )
            hr_str = hr + ":00-" + str(int(hr)+1) + ":00"
            if "available" in str(item) and hr_str in str(item):
                
                str_item = str(item)
                #print(str_item)
                soup2 = BeautifulSoup(str_item, 'html.parser')
                course_content = soup2.li["course_content"].split(",")
                APITool.order_dict["course_name[]"] = course_content[0]
                APITool.order_dict["hour[]"] = course_content[1]
                APITool.order_dict["price[]"] = course_content[2]
                APITool.order_dict["real_time[]"] = course_content[3]
                
                APITool.order_dict["goods_ids"] = soup2.li["goodsid"]
                APITool.doconfirm_dict["goods_ids"] = soup2.li["goodsid"]
                #print(APITool.order_dict)
                break
        
        input_list = soup.find_all("input")
        for item in input_list:
            str_item = str(item)
            if "book_date" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.order_dict["book_date"] = soup2.input["value"]
            if "allcourse_name" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.order_dict["allcourse_name"] = soup2.input["value"]
            if "court_name" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.order_dict["court_name"] = soup2.input["value"]
            if "category_name" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.order_dict["category_name"] = soup2.input["value"]
            if "bid" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.order_dict["bid"] = soup2.input["value"]
                APITool.doconfirm_dict["bid"] = soup2.input["value"]
                
        print("order_dict:")
        for key,value in APITool.order_dict.items():
            print(key,value)
#    
        
        print("Step complete!")
        print("")
        
        
    @classmethod
    def confirm_order(cls):  
        print("Step: confirm_order ")
        #whole_confirm_order_url =  APITool.add_get_info( APITool.order_dict )
        whole_confirm_order_url = URL.confirm_order_url + parse.urlencode( APITool.order_dict )
        print("whole_confirm_order_url: ", whole_confirm_order_url)
        response = cls.session.get( whole_confirm_order_url  )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        input_list = soup.find_all("input")
        for item in input_list:
            #print(str(item))
            #print("")
            str_item = str(item)
            if "J_payHash" in str_item:
                soup2 = BeautifulSoup(str_item, 'html.parser')
                APITool.doconfirm_dict["hash"] = soup2.input["value"]
        

        APITool.doconfirm_dict["_"] =  str(int (time.time() )*1000) 
        
        print("doconfirm_dict:")
        for key,value in APITool.doconfirm_dict.items():
            print(key,value)
        print("Step complete!")
        print("")

    @classmethod
    def doorder(cls):  
        print("Step: doorder ")
        #whole_confirm_order_url =  APITool.add_get_info( APITool.order_dict )
        whole_doconfirm_dict_url = URL.doorder_url +  parse.urlencode( APITool.doconfirm_dict )
        print("doorder_url: ",whole_doconfirm_dict_url )
        response = cls.session.get(whole_doconfirm_dict_url )
        
        print(response.json())
        
        print("Step complete!")
        print("")


if __name__ == '__main__':
    print(time.time())
    APITool.query_ticket()
    APITool.confirm_order()    
    APITool.doorder()
    print(time.time())
