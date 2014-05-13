# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:35:53 2014

@author: Max
"""

from webbrowser import open_new_tab 
from configparser import ConfigParser
from urllib.request import urlopen, unquote
from urllib.parse import urlencode
import json

class RenrenAPI():
    def __init__(self, config_file, access_token=""):
        """
        RenrenAPI初始化
        RenrenAPI用于使用人人网相关api
        
        :param config_file: 人人API相关值文件
        :param access_token: 初始化token值
        """
        
        self.log_message("RenrenAPI初始化中……")
        self.config_file = config_file
        self.access_token = access_token
        self.log_message("OK!", 0) 
         
    message_array = []
    
    def log_message(self,message,clear=True):
        """        
        Logs the message to the message_array, from where is
        retrieved to display in the console.
        
        :param message: The message string.
        :param clear: Buffer Clearane.
        """
        
        if clear:
            self.message_array = message
        else:
            self.message_array = "".join([self.message_array,message])
            
    def get_message(self):
        """
        Returns the log message to the console.
        
        :return: Returns the message.
        """
        
        return self.message_array
        
    def get_access_token(self,xrenew=False):
        """
        生成人人网认证请求链接
        
        :param config_file: 存有人人认证信息的配置文件路径
        :param xrenew: 如果此值为真，则会强制重新获取access_token,用于更换用户
        """
        
        #读取配置文件
        config = ConfigParser()
        config.read(self.config_file)
        
        #获取人人网认证信息
        url = config.get("Renren","URL")
        
        #拼接请求字段
        
        param = {   "client_id": config.get("Renren","API_KEY"),
                    "redirect_uri": config.get("Renren","REDIRECT_URI"),
                    "response_type": "token",
                    "display": "popup"
                }
        if xrenew:
            param["x_renew"] = "True"
            
        #生成请求链接  
        request = urlencode(param)
        r_url = "%s?%s" % (url,request)
        
        open_new_tab(r_url)
        self.access_token = unquote(input("请输入浏览器中的access_token：\n"))
    
    def user_friend_list(self, userId, pageSize, pageNumber):
        """
        获取某个用户的好友列表
        
        :param url: 请求地址
        :param userId: 用户ID
        :param pageSize: 页面大小（返回数量）
        :param pageNumber: 页码
        """
        
        url = "https://api.renren.com/v2/user/friend/list"
        param = {   "userId": userId,
                    "pageSize": pageSize,
                    "pageNumber": pageNumber,
                    "access_token": self.access_token
                }
        request = urlencode(param)
        r_url = "%s?%s" % (url, request)
        
        self.log_message("获取好友列表中(第{}页，每页{}个)……".format(pageNumber,
                                                                pageSize))
        response = urlopen(r_url)
        rep = response.read()
        rep = rep.decode("utf8")
        jcode = json.loads(rep)
        self.log_message("OK!", 0) 
        
        return jcode["response"]
    
    def user_login_get(self):
        """ 
        获取当前登录用户信息
        
        :param url: 请求地址
        """
        
        url = "https://api.renren.com/v2/user/login/get"
        param = {   "access_token": self.access_token,
                }
        request = urlencode(param)
        r_url = "%s?%s" % (url, request)
        
        self.log_message("正在获取当前登录用户信息……")
        response = urlopen(r_url)
        rep = response.read()
        rep = rep.decode("utf8")
        jcode = json.loads(rep)
        self.log_message("OK!", 0) 
        
        return jcode["response"]
        
    def user_get(self, userId):
        """ 
        获取用户信息
        
        :param url: 请求地址
        :param userId: 用户ID，不传时表示获取access_token对应的用户信息
        """
        
        url = "https://api.renren.com/v2/user/get"
        param = {   "access_token": self.access_token,
                    "userId": str(userId)
                }
        request = urlencode(param)
        r_url = "%s?%s" % (url, request)
        
        self.log_message("正在获取用户(ID={0})信息……".format(userId))
        response = urlopen(r_url)
        rep = response.read()
        rep = rep.decode("utf8")
        jcode = json.loads(rep)
        self.log_message("OK!", 0) 
        
        return jcode["response"]
    
    def profile_get(self, userId):
        """
        获取用户的主页信息，包括各种统计数据。
        
        :param url: 请求地址
        :param userId: 用户ID        
        """

        url = "https://api.renren.com/v2/profile/get"
        param = {   "access_token": self.access_token,
                    "userId": userId
                }
        request = urlencode(param)
        r_url = "%s?%s" % (url, request)
        
        self.log_message("正在获取用户的主页信息……")
        response = urlopen(r_url)
        rep = response.read()
        rep = rep.decode("utf8")
        jcode = json.loads(rep)
        self.log_message("OK!", 0)
        
        return jcode["response"]
    