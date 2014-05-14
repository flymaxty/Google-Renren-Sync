# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:35:53 2014

@author: Max
"""

from RenrenApi import RenrenAPI
from urllib.request import urlopen

#RenrenAPI初始化  
param = {}
renren = RenrenAPI("Config_ty.ini", debug=True)

#获取登录用户的信息
#renren.get_access_token(0)
user_info = renren.user.login.get()

#获取好友数量
param = {"userId" : user_info["id"]}
profile = renren.profile.get(param)
friendCount = profile["friendCount"]

#循环获取好友信息
pageSize = 50
pageNumber = 1
while pageSize*pageNumber < 60:
    
    #获取好友列表
    param = {
            "userId" : user_info["id"],
            "pageSize" : pageSize,
            "pageNumber" : pageNumber
            }
    friends_list = renren.user.friend.list(param)
    
    for item in friends_list:
        #根据ID获取好友个人信息
        param = {"userId" : item["id"]}
        friend_info = renren.user.get(param)
        
        #生成头像文件名        
        path1 = r".\image""\\"
        friend_name = friend_info["name"]        
        try:
            friend_birthday = friend_info["basicInformation"]["birthday"]
            if friend_birthday == "0-0-0":
                raise Exception
        except Exception :
            print("用户没有生日信息！！")
            friend_birthday = "Unknown"
        path2 = "{0}({1})".format(friend_name, friend_birthday)
        file_path = path1 + path2 + ".jpg"
        
        #获取好友头像地址
        url = friend_info["avatar"][3]["url"]
        
        #开始获取
        print("正在获取{0}的头像……".format(friend_info["id"]),end="")
        response = urlopen(url).read()
        file = open(file_path,"wb")
        file.write(response)
        file.close
        print("ok!")
        
        pageNumber = pageNumber + 1
    
    print("Everything is down!")