# -*- coding: utf-8 -*-
# __author__ = 'lusn'

import time
import datetime
#  首先将时间字符串处理成标准的，即将小数位去掉
time_stamp = "2019-04-10 00:30:10.198" .split('.')[0]
print(time_stamp)
#  将字符串转化为时间戳
h =  time.mktime(time.strptime(time_stamp, "%Y-%m-%d %H:%M:%S"))
print(h)
#  将时间戳转换为字符串
start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(h-30))
print(start_time)
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(h+30))
print(end_time)
#  将时间字符串转化为datetime类型
start_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
print(start_date)

#  将时间戳转化为datetime类型
t = datetime.datetime.fromtimestamp(h)
print(t,type(t))

print(start_date,type(start_date))

#时间戳

t = time.time()
print (t)                       #原始时间数据
print (int(t))                  #秒级时间戳
print (int(round(t * 1000)))    #毫秒级时间戳
print (int(round(t * 1000000))) #微秒级时间戳

import random
print("12345")

print("==================================")
print(time.time())
print(time.ctime())
print(time.localtime())
print(time.strftime("%Y-%m-%d %H_%M_%S"))
print(time.strftime("%Y-%m-%d_%H_%M_%S"))