# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:35:53 2014

@author: Max
"""

from RenrenApi import RenrenAPI
from urllib.request import urlopen

#RenrenAPI初始化  
renren = RenrenAPI("Config.ini", access_token)
print(renren.get_message())

#获取登录用户的信息
user_info = renren.user_login_get()
print(renren.get_message())

#获取好友数量
user_id = user_info["id"]
profile = renren.profile_get(user_id)
print(renren.get_message())
friendCount = profile["friendCount"]

#循环获取好友信息
i = 0
while 50*i < friendCount:
    i = i+1
    
    #获取好友列表
    friends_list = renren.user_friend_list(user_id, 50, i)
    print(renren.get_message())
    
    for item in friends_list:
        #根据ID获取好友个人信息
        user_info = renren.user_get(item["id"])
        print(renren.get_message())
        
        #生成头像文件名        
        path1 = r".\image""\\"
        user_name = user_info["name"]        
        try:
            user_birthday = user_info["basicInformation"]["birthday"]
            if user_birthday == "0-0-0":
                raise Exception
        except Exception :
            print("用户没有生日信息！！")
            user_birthday = "Unknown"
        path2 = "{0}({1})".format(user_name, user_birthday)
        file_path = path1 + path2 + ".jpg"
        
        #获取好友头像地址
        url = user_info["avatar"][3]["url"]
        
        #开始获取
        print("正在获取{0}的头像……".format(user_info["id"]),end="")
        response = urlopen(url).read()
        file = open(file_path,"wb")
        file.write(response)
        file.close
        print("ok!")
    
    print("Everything is down!")