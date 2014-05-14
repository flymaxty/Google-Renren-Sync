# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:35:53 2014

@author: Max
"""
from os import mkdir
from os.path import exists
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

#创建image目录
path = r".\image\\"
if not exists(path):
    mkdir(path)

#循环获取好友信息
renren.debug = False
number = 1
pageSize = 50
pageNumber = 0

while pageSize*pageNumber < friendCount:
    
    pageNumber += 1
    
    #获取好友列表
    param = {
            "userId" : user_info["id"],
            "pageSize" : pageSize,
            "pageNumber" : pageNumber
            }    
    friends = renren.user.friend.list(param)
    
    friends_list = []
    for item in friends:
        friends_list.append(str(item["id"]))

    param = {"userIds" : ",".join(friends_list)}
    friends_info = renren.user.batch(param)
    
    for item in friends_info:
        
        #生成头像文件名
        friend_name = item["name"]
        try:
            friend_birthday = item["basicInformation"]["birthday"]
            if friend_birthday == "0-0-0":
                raise Exception
        except Exception :
            friend_birthday = "Unknown"
        path2 = "{0}-{1}({2})".format(number, friend_name, friend_birthday,)
        file_path = path + path2 + ".jpg"
        
        #获取好友头像地址
        url = item["avatar"][3]["url"]
        
        #开始获取
        print("正在获取第{0}/{1}个头像……".format(number,friendCount))       
        response = urlopen(url).read()
        file = open(file_path,"wb+")
        file.write(response)
        file.close
        
        number += 1

print("完成")