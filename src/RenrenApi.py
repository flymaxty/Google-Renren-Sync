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
import time
import sys

class RenrenAPI():
    def __init__(self, config_file="Config.ini", debug=False):
        """
        RenrenAPI初始化
        RenrenAPI用于使用人人网相关api
        
        :param config_file: 人人API相关值文件
        :param info : 存放人人API相关参数
        :param r_url: 用于存放请求地址
        """
        self.debug = debug        
        self.log_message("RenrenAPI初始化中……")
        self.config_file = config_file
        self.r_url = ""
        
        #读取配置文件
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.info = {"APP_ID": self.config.get("Renren","app_id"),
                     "API_KEY": self.config.get("Renren","api_key"),
                     "SECRET_KEY": self.config.get("Renren","secret_key"),
                     "AUTHORIZE": self.config.get("Renren","authorize"),
                     "API_URL": self.config.get("Renren","api_url"),
                     "REDIRECT_URL": self.config.get("Renren","redirect_url"),
                     "ACCESS_TOKEN": self.config.get("Renren","access_token")
                    }

        self.log_message("OK!") 
    
    def log_message(self,message):
        """        
        Logs the message to the message_array, from where is
        retrieved to display in the console.
        
        :param message: The message string.
        """
        
        if self.debug == True:
            ctime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(ctime + "  " + message)

    def get_access_token(self,xrenew=False):
        """
        生成人人网认证请求链接
        
        :param xrenew: 如果此值为真，则会强制重新获取access_token,用于更换用户
        """
        
        #获取人人网认证信息
        url = self.info["AUTHORIZE"]

        #拼接请求字段
        
        param = {   "client_id": self.info["API_KEY"],
                    "redirect_uri": self.info["REDIRECT_URL"],
                    "response_type": "token",
                    "display": "popup"
                }
        if xrenew:
            param["x_renew"] = "True"
            
        #生成请求链接  
        request = urlencode(param)
        r_url = "%s?%s" % (url,request)
        
        open_new_tab(r_url)
        self.info["ACCESS_TOKEN"] = \
            unquote(input("请输入浏览器中的access_token：\n"))
        self.config.set("Renren", "access_token", self.info["ACCESS_TOKEN"])          

    def url_wrapper(self,attr):
        """
        请求地址封装
        
        :param attr:请求参数
        :param r_url:请求地址
        """
        
        self.r_url = "%s/%s" % (self.r_url, attr)
        
        return self
    
    def request(self, request_list):
        """
        请求函数
        
        :param request_list: 请求参数列表
        """

        #请求链接生成     
        request_list["access_token"] = self.info["ACCESS_TOKEN"]
        url = self.info["API_URL"] + self.r_url
        url = "%s?%s" % (url, urlencode(request_list))
        
        #发起请求
        self.log_message("Requesting({0})....".format(self.r_url)) 
        try:        
            response = urlopen(url)
        except Exception as error:
            #异常处理
            code = str(error.code)
            reason = str(error.reason)
            self.log_message("HttpError {0} : {1}".format(code, reason))
            content = error.read()
            content = content.decode("utf8")
            jcode = json.loads(content)
            message = jcode["error"]["message"]
            self.log_message(message)
            
            #抛出异常
            raise Exception("RenrenApi Error: " + message)
            
        content = response.read()
        content = content.decode("utf8")
        jcode = json.loads(content)
        self.log_message("OK!")
        
        #清空r_url请求字段
        self.r_url = ""
        
        return jcode["response"]
        
    def __getattr__(self, attr):
        return self.url_wrapper(attr)
    
    def __call__(self, key={}):
        return self.request(key)
        
    def __del__(self):
        #保存更改的参数
        self.config.write(open(self.config_file, "w"))
        
if __name__ == "__main__":
    renren = RenrenAPI("config_ty.ini", debug=True)
    
    renren.get_access_token(0)
    
    info = renren.user.login.get()
    print(info["name"])