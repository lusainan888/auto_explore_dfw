# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#1、多个字典==>列表
# a={'gameId': 136165, 'basePlayId': 23987, 'centring': 'true', 'decentered': 'false'}
# b={'gameId': 136161, 'basePlayId': 23987, 'centring': 'true', 'decentered': 'false'}
# c={'gameId': 136163, 'basePlayId': 23987, 'centring': 'true', 'decentered': 'false'}
# #多个字典变列表
# y=[a,b,c]
# print("3个字典转列表：",y,'\n')
#
# #2、列表添加元素
# list = []          ## 空列表
# list.append('Google')   ## 使用 append() 添加元素
# list.append('Runoob')
# print ("添加元素后的列表：",list,'\n')
#
# #3、读取txt  替换txt  写入txt
# import os,sys,json
# file = os.getcwd()+'\playid.txt'
# f = open(file,'r')
# body = f.read()
# body=json.loads(body)
# print("初始模板",body,type(body))  #读取txt中字典
#
# gameId=[136161]
# list=[23961, 23962]
# body['gameId']=gameId[0]     #替换字典值,生成新字典
# body['basePlayId']=list[0]
# print("最终模板",body)
# #修改后内容写入txt
# f.close()
#
# #4、ASCII转为Native
# name = "\\u6697\\u88d4\\u5251\\u9b54"
# name1= "\\u5f20\\u4e09"
# print(name.encode().decode('unicode_escape'),'\n',name1.encode().decode('unicode_escape'))

#5、get\post请求  未完
# Content-Type的格式有四种：分别是application/x-www-form-urlencoded（这也是默认格式）、
#                               application/json、
#                               text/xml
#                               以及multipart/form-data格式。
import json
import requests
import http.client
import urllib
import urllib.parse
#1.1、get-没有参数-requests库
# res = requests.get("http://httpbin.org/get")
# print("request-get",res.text) # 自动按默认utf-8解码

#1.2、get-无参数-http.client库
# conn = http.client.HTTPConnection("httpbin.org")  #建立http连接
# conn.request("GET", '/get')  #发送get请求，指定接口路径
# res = conn.getresponse()     #获取响应
# print(res.read().decode('utf-8')) # 自己解码 http.client  str转bytes叫encode，bytes转str叫decode

#1.3、get-无参数-urllib.request库
# res = urllib.request.urlopen("http://httpbin.org/get")
# print(res.read().decode("utf-8")) # 自己解码

#2.1、get-有参数-requests库
# res = requests.get("http://httpbin.org/get?name=张三&age=12")
# print("request-get",res.text) # 自动按默认utf-8解码
# d=json.loads(res.text)   #字符串转化为字典  已经ASCII转为Native
# name=d["args"]['name']
# print(name)

#2.2、get-有参数-http.client库
# conn = http.client.HTTPConnection("httpbin.org")  #建立http连接
# url = urllib.parse.quote("/get?name=张三&age=12", safe=':/?=&') # 进行url编码
# conn.request("GET", url)  #发送get请求，指定接口路径  url编码
# res = conn.getresponse()     #获取响应
# print(res.read().decode('utf-8')) # 自己解码     http.client  str转bytes叫encode，bytes转str叫decode

#2.3、get-有参数-urllib.request库
# url=urllib.parse.quote("http://httpbin.org/get?name=张三&age=12",safe=' :/?=&')
# print(url)
# res = urllib.request.urlopen(url)  #url编码
# print(res.read().decode("utf-8")) # 自己解码           3、urllib.request


#3、post-request库
# #########A、application/x-www-form-urlencoded##########
# data = {"name":"张三", "age": 12}
# res = requests.post("http://httpbin.org/post", data=data) # 自动编码
# print(res.text)

#########B、application/json##########
# data = {"name":"张三", "age": 12}
# res = requests.post("http://httpbin.org/post", json=data)
# # print(res.text)
# print(res.json())  # 转为字典格式
##########C、 text/xml##########
# xml = """my 22222 xml"""
# xml=  '<?xml version="2.0" encoding = "UTF-8"?>' \
#       '<COM>' \
#       '<REQ name="北京-宏哥">' \
#       '<USER_ID></USER_ID>' \
#       '<COMMODITY_ID>123456</COMMODITY_ID>' \
#       '<SESSION_ID>absbnmasbnfmasbm1213</SESSION_ID>' \
#       '</REQ>' \
#       '</COM>'
# headers = {'Content-Type': 'text/xml'}
# res=requests.post('http://httpbin.org/post', data=xml.encode("utf-8"), headers=headers)
# # print(res.text)
# print(res.text.encode().decode('unicode_escape'))

#从xml文件读取data
# with open('body.xml',encoding='utf-8') as fp:
#     xml = fp.read()
# headers = {'Content-Type': 'text/xml'}
# res=requests.post('http://httpbin.org/post', data=xml.encode("utf-8"), headers=headers)
# print(res.text.encode().decode('unicode_escape'))

##########D、 multipart/form-data##########
# url = 'http://httpbin.org/post'
# # files = {'file': open('report.xls', 'rb')}
# files = {'file': open('D:\\auto_test_nancy\\coingame\\data\\report.xls', 'rb')}
# r = requests.post(url, files=files)
# print(r.text)

#6、普通加法器
# -*- coding: utf-8 -*-
# __author__ = 'lusn'
def sum(a,b):
    sum=a+b
    return sum
print (sum(2,4))

def sum(a=2,b=3):
    sum=a+b
    c=99
    print (c)
    return sum
print (sum(4,9))

print("6 类的实例化举例")
#-*- coding: utf-8 -*-
#__author__ = 'lusn'
class Student1:
    def __init__(self):#两者之间的区别
        self.name = "helen"
        self.score = 60
    def print_score1(self):
        print("%s score is %s" % (self.name, self.score))

    def get_grade1(self):
        if self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        else:
            return "C"
susan=Student1()
susan.name="tom"
susan.score=60
susan.print_score1()
print(susan.get_grade1())


class Student2:
    def __init__(self,name,score):#两者之间的区别    #第一个参数必须是self
        self.name = name           #类属性
        self.score = score
    def print_score2(self):      #函数必须传入self，self用于区分是哪个对象调用该方法！！！
        print("%s score is %s" % (self.name, self.score))

    def get_grade2(self):
        if self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        else:
            return "C"
# mary=Student2("tom",90) #实例化类
name="jack"
score=88
mary=Student2(name,score)
mary.print_score2()
print(mary.get_grade2())


class Student3:
    def __init__(self,name="nancy",score=99):#两者之间的区别
        self.name = name           #类属性
        self.score = score
        print("%s 的 score is %s" % (self.name, self.score))
    def get_grade3(self):
        if self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        else:
            return "C"
jack=Student3()
print(jack.get_grade3())

# coding=utf-8
class Student:
    def __init__(self,name,age):
        self.name  = name
        self.age = age
    def GetName(self):
        return self.name

    def GetAge(self):
        return self.age
if __name__ == '__main__':
    person = Student("reacher",18)
    print(person.GetName(),person.GetAge())

# #7、selenuim  例子1
# # 百度selenium例子   chrome版本 79.0.3945.88（正式版本) selenuim 3.14.1
# # -*- coding: utf-8 -*-
# # __author__ = 'lusn'
#
#
# import time
# from selenium import webdriver
# search_text = ['python', '中文', 'text']
# for text in search_text:
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(10)
#     driver.get("http://www.baidu.com")
#     driver.find_element_by_id('kw').send_keys(text)
#     driver.find_element_by_id('su').click()
#     time.sleep(2)
#     driver.quit()
#
# #selenuim  例子2
# #注册用户+模块化+数据驱动，实现所有注册，测试用例
# import time
# import unittest
# from selenium import webdriver
# import random
# from selenium.webdriver.common.action_chains import ActionChains
# class LoginTest(unittest.TestCase):
#     '''注册'''
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#
#     def test_login(self):
#         driver=self.driver
#         driver.get("http://testing-www.intranet.dcml.com/home")
#         #区号选择
#         double_click=driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[1]/div/div")
#         ActionChains(driver).double_click(double_click).perform()
#         time.sleep(1)
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[1]/div/ul/li[1]/div").click()#KR  li[1]CN  li[2]US li[3]
#         #手机号
#         #driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[2]/div[2]/input").send_keys("15009990361")
#
#         list=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
#         shou=( random.choice(list))
#         wo=str(random.randint(00000000,99999999))
#         wei=wo.zfill(8)
#         tel=shou+wei
#         print(tel)
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[2]/div[2]/input").send_keys(tel)
#
#         #密码
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[3]/div[2]/input").send_keys("11111111")
#         #重复密码
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[4]/div[2]/input").send_keys("11111111")
#         #验证码
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[5]/div[2]/div/div/button").click()
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[5]/div[2]/div/input").send_keys("123456")
#         #协议
#         '''
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[6]/div[1]/img").click()
#         time.sleep(1)
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/
#         orm/div[6]/div[1]/img").click()
#         '''
#         #提交
#         driver.find_element_by_xpath(".//*[@id='app']/div/div/div/div/div[1]/div[3]/div/div/form/div[7]/button").click()
#         '''
#         title=driver.title
#         self.assertEqual(title,"Coin&Cash - 数字货币抵押贷款-基于智能合约打造的数字资产抵押贷款平台") #断言
#         print(title)
#         '''
#     def tearDown(self):
#         time.sleep(2)
#         self.driver.quit()
#
# if __name__ == "__main__":
#     unittest.main()

#8、线程延时5s执行
# encoding: UTF-8
# import threading
# def func():
#     print ('hello timer!')
# timer = threading.Timer(5, func)
# timer.start()
#

#