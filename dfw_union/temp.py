# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#1、全局变量的修改必须加锁（阻塞---效率低) threading.local()
#2、threading.local()虽然是局部变量，但每个线程都只读写自己线程的独立副本，互不干扰
import threading
import time
from datetime import datetime
from public.common.SHAtools import sha256hex
#########！！多线程运用！！################
# ##############1##############
# #多线程局部变量之threading.local()  或者加锁
# thread_local_obj = threading.local()  #实例化一个对象 threading.local()的作用就是为每个线程开辟一个独立的空间进行数据存储。
#
# class TestClass:
#     def __init__(self, num):
#         self.num = num
#
# global_var = 0
# def testfn(num, obj):    #线程函数
#     global  global_var
#     global_var = num
#     local_var = num * 2
#     obj.num = num * 2
#     thread_local_obj.obj = obj
#     time.sleep(5)
#
#     other_task()  #线程函数调用另一个函数
#
#     print("thread id:", threading.get_ident(), 'num:', num, 'obj.num:', obj.num, 'local_var:', local_var, 'global_var:', global_var)
#
# def other_task():
#     #拎一个函数：比如读取和线程关联的对象的属性值、修改属性值
#     print("thread id:", threading.get_ident(), 'obj.num:', thread_local_obj.obj.num , threading.currentThread().name)
#
#
# for i in range(0, 3):
#     # # 多线程执行性能监控
#     #两个以上的线程访问全局变量时，就会出现所谓的“不安全"
#     thread = threading.Thread(target=testfn,name="testfn"+str(i),args=(i, TestClass(i)))
#     thread.start()
#




# ##############2##############
# # 创建全局ThreadLocal对象
# local_school = threading.local()
# class Student():
#     def __init__(self, name):
#         self.name = name
#
# def process_student(name):
#     std = Student(name)
#     local_school.student = std   # 写操作
#    # local_school.teacher = std
#     do_task_1()
#     do_task_2()
#
# def do_task_1():
#     std = local_school.student  # 读操作
#     print("do_task_1", std.name)
#
# def do_task_2():
#     std = local_school.student   # 读操作
#     print("do_task_2", std.name)
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=process_student, args=("Curry",))
#     t2 = threading.Thread(target=process_student, args=("大雄",))
#     t1.start()
#     t2.start()
# #
# ##############3##############import time
# class MyThread(threading.Thread):
#     def run(self):
#         global num
#         time.sleep(1)
#
#         if mutex.acquire(1):   #获取锁
#             num = num+1
#             msg = self.name+' set num to '+str(num)
#             print (msg)
#             mutex.release()#释放锁
# num = 0
# mutex = threading.Lock()
# def test():
#     for i in range(5):
#         t = MyThread()
#         t.start()
# if __name__ == '__main__':
#     test()


###############4###############
import threading
import time
#
# # class A:
# #     def __init__(self,x):
# #         self.x = x
# # a = A(0)
#
# a = threading.local()#全局对象
#
# def worker():
#     a.x = 0
#     for i in range(100):
#         time.sleep(0.0001)
#         a.x += 1
#     print(threading.current_thread(),a.x)
#
# for i in range(10):
#     threading.Thread(target=worker).start()
#

###############6####################
'''
    多线程操作全局变量 使用互斥锁
    重点：声明一个全局互斥锁
'''
import threading
import time

counter = 0
mutex = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global counter, mutex
        time.sleep(1);
        if mutex.acquire():
            counter += 1
            print("I am %s, set counter:%s,time is:%s" % (self.name, counter,datetime.now()))
            mutex.release()

if __name__ == "__main__":
    for i in range(0, 100):
        my_thread = MyThread()
        my_thread.start()
'''
###########5、4的运用############  NG
import json
import requests
import threading
import time

extraHash=sha256hex("999")
counter = 0
mutex = threading.Lock()#全局对象

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def post_up_unoin2(self):
            global counter, mutex
            if mutex.acquire():
                counter += 1
                hash=MyThread.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt",info='rw')
                print(hash)
            # print(threading.current_thread(),hash)
            # headers={"Content-Type":"application/json"}
            # url='http://172.17.3.121:9091'+'/chain/file/create'
            # data ={"hash":hash,"extraHash":extraHash}
            # data =json.dumps(data)  #dic-->str
            # start = datetime.now()
            # r = requests.post(url=url,data=data,headers=headers)
            # info=json.dumps(r.text) #将字典转化为字符串
            # d=json.loads(r.text)  #字符串转化为字典
            # print("message:",d["message"])
    def run(self):
        global counter, mutex
        time.sleep(1)
        if mutex.acquire():
            counter += 1
            print ("I am %s, set counter:%s" % (self.name, counter))
            mutex.release()

    def read_write_info(self,file_path,info=None):
        """向文件写或读取信息"""
        if info==None:
            fp = open(file_path,'r',encoding='utf8')    #读 None
            return fp.read()
        elif info=="rw":
            fp = open(file_path,'r',encoding='utf8')    #读取，每次读取txt新值，再+1存入txt，下次利用
            s = fp.read()
            text = int(s)
            # f.close()
            f = open(file_path,'w')
            f.write(str(text+1))
            # f.close()
            file_hash=sha256hex(s)
            # return str(hash)
            return file_hash

        else:
            # self.info=hash   ##写入新的hash用
            # fp = open(file_path,'w',encoding='utf8')
            fp = open(file_path,'a+',encoding='utf8')  #写 info
            fp.write(self.info+"\n")
        fp.close()

if __name__ == "__main__":
    for i in range(0, 1):
        my_thread = MyThread()
        my_thread.start()
'''

##Python3-多线程共享全局变量
from threading import Thread
import time,random

g_num = 100

def work1():
    global g_num
    for i in range(3):
        g_num += 1
        time.sleep(random.random())
        print("in work1,g_num=%d" % g_num)


def work2():
    global g_num
    for i in range(3):
        g_num += 1
        time.sleep(random.random())
        print("in work2,g_num=%d" % g_num)


if __name__ == "__main__":

    t1 = Thread(target=work1)
    t2 = Thread(target=work2)

    t1.start()
    t2.start()
