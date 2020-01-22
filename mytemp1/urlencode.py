# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#python3  urllib.parse模块
from urllib.parse import unquote, unquote_plus,urlencode,quote

#encoded_url = 'https://testing-sp-sso.dae.org/uaa/oauth/authorize?response_type=token&client_id=www&redirect_uri=https%3A%2F%2Ftesting-sp-www.dae.org%2Fhome%2Fmember%2Fmain&state=%2Fhome%2Fmember%2Fmain'
encoded_url='http://172.17.3.187:8080/api/blockAndTxList/3ccdd2d12947951abebd8ca870457e5d3a716a318548d01f3f74d369c6d329a1/0?from=Thu%20Jan%2002%202020%2021:05:50%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&&to=Wed%20Jan%2015%202020%2019:09:50%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
print("url解密:",unquote(encoded_url))
# print(unquote_plus(encoded_url))

decoded_url ='http://10test97-wap.stg3.1768.com/?act=external_coingame&st=payNotify&web=1&gameId=4104'
data=quote(decoded_url)
print ("url加密:",data)

'''
#urlencode与urldecode
import urllib.parse
values={}
values['username']='02蔡彩虹'
values['password']='ddddd?'
print ("values is: %s" %values)

url="http://www.baidu.com"
data=urllib.parse.urlencode(values)
print("data is :%s" %data)   #url encode


s='长春'
s=urllib.parse.quote(s)
print("s is :%s" %s)         #字符串encode

s='%E5%B9%BF%E5%B7%9E'
s=urllib.parse.unquote(s)
print("s_decode is %s" %s)   #字符串decode

s='username=02%E8%94%A1%E5%BD%A9%E8%99%B9&password=ddddd%3F'
s=urllib.parse.unquote(s)
print("s_decode is %s" %s)   #字符串decode

'''

'''
import urllib.parse
s='http://10test97-wap.stg3.1768.com/?act=external_coingame&st=payNotify&web=1&gameId=4104'
s=urllib.parse.quote(s)
print("s is :%s" %s)         #字符串encode

s='http%3A//10test97-wap.stg3.1768.com/%3Fact%3Dexternal_coingame%26st%3DpayNotify%26web%3D1%26gameId%3D4104'
s=urllib.parse.unquote(s)
print("s is :%s" %s)         #字符串encode
'''


#基于python2
# -*- coding:utf-8 -*-
# __author__ = 'lusn'
#python2 urllib 模块

# from urllib import unquote, unquote_plus,urlencode,quote
# encoded_url = 'https://testing-sp-www.dae.org/mobile/rechangeCoin?code=SfeI3K&version=v1.0.0&user=U-2qL1nJ&channelId=04009&redirectUrl=http%3A%2F%2F10test97-wap.stg3.1768.com%2F%3Fact%3Dexternal_coingame%26st%3DpayBack&callbackLink=http%3A%2F%2F10test97-wap.stg3.1768.com%2F%3Fact%3Dexternal_coingame%26st%3DpayNotify%26gameId%3D40038'
# print("url解密:"+unquote(encoded_url))
# # print(unquote_plus(encoded_url))   #decode
#
# decoded_url ='https://tst10-97-wap-stg3.1768.com/?act=external_coingame&st=payNotify&gameId=4260'
# data=quote(decoded_url)
# print ("url加密:"+data)        #encode
'''
#urlencode与urldecode
import urllib
values={}
values['username']='02蔡彩虹'
values['password']='ddddd?'
print ("values is: %s" %values)

url="http://www.baidu.com"
data=urllib.urlencode(values)
print("data is :%s" %data)   #url encode


s='长春'
s=urllib.quote(s)
print("s is :%s" %s)         #字符串encode

s='%E5%B9%BF%E5%B7%9E'
s=urllib.unquote(s)
print("s_decode is %s" %s)   #字符串decode

s='username=02%E8%94%A1%E5%BD%A9%E8%99%B9&password=ddddd%3F'
s=urllib.unquote(s)
print("s_decode is %s" %s)   #字符串decode

'''
'''
import urllib
s='http://10test97-wap.stg3.1768.com/?act=external_coingame&st=payNotify&web=1&gameId=4104'
s=urllib.quote(s)
print("s is :%s" %s)         #字符串encode

s='http%3A//10test97-wap.stg3.1768.com/%3Fact%3Dexternal_coingame%26st%3DpayNotify%26web%3D1%26gameId%3D4104'
s=urllib.unquote(s)
print("s is :%s" %s)         #字符串encode
'''