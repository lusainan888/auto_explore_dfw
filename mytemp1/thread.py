# -*- coding: utf-8 -*-
# __author__ = 'lusn'
# #1、循环
# def jishu():
#     print(i)
# if __name__ == '__main__':
#     for i in range(3):  #get循环5次
#         i=i+1
#         a=jishu()
#
#2、多线程并发
import threading
import time
from datetime import datetime
#
# def thread_func(threadID):  # 线程函数
#     #print('我是一个线程函数。')
#     print("调用时间:", datetime.now(),threadID)
#     time.sleep(1)
#     #print("返回时间:", datetime.now(),"\n")
#
# def execute_func(m):
#     for v in range(m):
#         print("调用时间:", datetime.now())
#         time.sleep(1)
#         # thread_func()
#         # print("v",v)
#         # print("kv",k+v)
# def many_thread(n,m):
#     start = datetime.now()
#     print("start:",start)
#     threads = []
#     threadID=0
#     for k in range(n):  # 循环创建500个线程   5个线程每个循环3次
#         threadID +=1
#         t = threading.Thread(target=execute_func, args=(m,))  #execute_func 创建线程          t = threading.Thread(target=execute_func, args=[3])
#         #t = threading.Thread(target=thread_func,args=(threadID,))
#         # t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
#         # execute_func(1)
#         # t.start()
#         threads.append(t)  #添加线程到线程组
#     #print("threads",threads)  #Thread-5
#     for t in threads:
#         t.start()  #开启线程
#     for t in threads:
#         t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
#     print('主线程结束了！' , threading.current_thread().name)
#     duration = datetime.now() - start
#     print("duration:",duration)
#
# if __name__ == '__main__':
#     #5个线程循环2遍
#     many_thread(5,2)   #线程数、循环数  (启动5个线程)  500,2 duration: 0:00:00.070810 /50 20 duration: 0:00:00.019915

#同上
# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#、多线程并发
# import threading
# import time
# from datetime import datetime
#
# def thread_func(n,m):  # 线程函数
#     #print('我是一个线程函数。')
#     # print("调用时间:",n,m,datetime.now())
#     time.sleep(1)
#     # print("返回时间:", datetime.now(),"\n")
#
# def execute_func(n,m):
#     for _ in range(m):
#         thread_func(n,m)
#
# def many_thread(n,m):
#     start = datetime.now()
#     print("start:",start)
#     threads = []
#     for _ in range(n):  # 循环创建500个线程   n个线程每个循环m次
#         t = threading.Thread(target=execute_func, args=(n,m))  #execute_func 创建线程          t = threading.Thread(target=execute_func, args=[3])
#         # t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
#         threads.append(t)  #添加线程到线程组
#     # print("threads",threads)  #Thread-5
#     for t in threads:
#         t.start()  #开启线程
#     for t in threads:
#         t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
#     print('主线程结束了！' , threading.current_thread().name)
#     duration = datetime.now() - start
#     print("duration:",duration)
#
# if __name__ == '__main__':
#     many_thread(10,3)   #线程数、循环数  (启动5个线程)  #这个多线程是OK的
# #

# from datetime import datetime
# import requests
# import json
# import threading
# import time
# import uuid
# class postrequests():
#     def __init__(self):
#         #产生UUID
#         u = uuid.uuid1()
#         #产生订单编号
#         orderID = 'TEST' + u.hex
#         self.url = 'http://123.57.210.36:8091/couponWeb/couponSX/comboCouponOrderFrozen'
#         self.data = {"payOrderNo": orderID,"userId":"16500","activityId":"1103",
#                      "couponIdNumMap":{"2580":2,"2581":2,"2582":2}}
#         self.headers = {'content-type': 'application/json'}
#         self.data = json.dumps(self.data)
#
#     def post(self):
#         try:
#             r = requests.post(self.url, self.data, headers=self.headers)
#             print(r.text)
#         except Exception as e:
#             print(e)
#
# def kquan_bf():
#     login = postrequests()
#     return login.post()
#
#
# try:
#     i = 1
#     # 开启线程数目
#     tasks_number = 10
#     print('测试启动')
#     time1 = time.clock()
#     # time1=datetime.now()
#     print("time1",time1)
#     while i < tasks_number:
#         t = threading.Thread(target=kquan_bf)
#         t.start()
#         i +=1
#         # time.sleep(0.1)
#     time2 = time.clock()
#     # time2=datetime.now()
#     times = time2 - time1
#     print("time2",time2)
#     print('所有线程启动的平均时间差',times/tasks_number)  #0:00:00.900910 9S多 0.9011490500000001
# except Exception as e:
#     print(e)
# if __name__ == '__main__':
#     kquan_bf()


#多线程  互斥锁Lock
# import threading,time
# lock=threading.Lock()
# n=0
# def func():
#     #开始处理数据
#     global n
#     lock.acquire() #获取  用于线程同步
#     a=n+1
#     time.sleep(0.0001)
#     n =a
#     lock.release() #释放
#     # 结束处理
#
# def thread():
#     li =[]
#     start=datetime.now()
#     for i in range(1000):
#         t=threading.Thread(target=func,args=())
#         li.append(t)
#         t.start()
#     for i in li:
#         i.join()  #等待子线程全部执行完
#     duration = datetime.now() - start
#     # print("duration2:",duration)
#     # print(n)  #253
#
# if __name__ == '__main__':
#     thread()   #1000


#多线程  提升1+2+...+100的速度

#多线程  提示下载图片速度  略
#多线程  提示写入数据、读取数据速度 略
#多线程 完成俩独立任务，速度提升7S-->4S
# import thread
# from time import sleep,ctime
# def loop0():
#     # print ('start loop0','at:',ctime())
#     start=datetime.now()
#     sleep(4)
#     # print ('loop0','done at:',ctime())
#     duration=datetime.now() - start
#     print("loop0 duration:",duration)
#
# def loop1():
#     # print( 'start loop1','at:',ctime())
#     start=datetime.now()
#     sleep(3)
#     # print('loop1','done at:',ctime())
#     duration=datetime.now() - start
#     print("loop0 duration:",duration)
#
# def main():
#     print( 'starting at:',ctime())
#     loop0()
#     loop1()
#     print ('all done at:',ctime())
#
# if __name__=='__main__':
#     main()   #4+3=7S
# #改进 缩成4s
# import threading
# from time import sleep,ctime
# loops =[4,3]
# def loop(nloop,nsec):
#     # print ('start loop',nloop,'at:',ctime())
#     sleep(nsec)
#     # print ('loop',nloop,'done at:',ctime())
# def main():
#     # print ('starting at:',ctime())
#     start=datetime.now()
#     threads = []
#     nloops = range(len(loops))
#     for i in nloops:
#         t = threading.Thread(target=loop,args=(i,loops[i]))
#         threads.append(t)
#
#     for i in nloops:
#         # print ('thread',i,'start')
#         threads[i].start()
#
#     for i in nloops:
#         # print ('thread',i,'join')
#         threads[i].join()
#
#     # print ('all done at:',ctime())
#     duration=datetime.now() - start
#     print("main duration:",duration)
# if __name__=='__main__':
#     main()
#

#多线程写入文件
import random
from public.common.SHAtools import sha256hex
from dfw_union.union import union

# start=datetime.now()
# def new_hash(n):
#     #生成100条hash，插入文件
#     if n==1:
#         for i in range(0,1000):  #False 传   0:00:01.626657/100       0:00:16.588621/1000
#             hash=sha256hex("东方新闻news4"+str(i))
#             info=hash
#             o=union()
#             o.read_write_info("C:\\software\\apache-jmeter-4.0\\bin\\lsn\\script\\newhash1.txt",info)
#         # print("全新hash ",i+1,"条生成完毕！！")
#         # print("耗时：",datetime.now()-start)
#     else:
#         t = time.time()
#         Fhash=str(random.randint(0,99999999))+str(round(t * 1000))
#         hash=sha256hex(Fhash)
#         o=union()
#         o.read_write_info("C:\\software\\apache-jmeter-4.0\\bin\\lsn\\script\\newhash1.txt",hash)
# def many_thread(n):
#     start = datetime.now()
#     print("start:",start)
#     threads = []
#     for _ in range(n):  # 循环创建500个线程   n个线程每个循环m次
#         t = threading.Thread(target=new_hash, args=(n,))  #execute_func 创建线程          t = threading.Thread(target=execute_func, args=[3])
#         # t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
#         threads.append(t)  #添加线程到线程组
#     # print("threads",threads)  #Thread-5
#     for t in threads:
#         t.start()  #开启线程
#     for t in threads:
#         t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
#     print('主线程结束了！' , threading.current_thread().name)
#     duration = datetime.now() - start
#     print("duration:",duration)
#     #
# if __name__ == '__main__':
#     pass
#     # new_hash()
#     # many_thread(1)  #明显提升 duration: 0:00:00.292179
#     # many_thread(1000)  #明显提升 duration: 0:00:00.292179

#多线程读取文件
start=datetime.now()
def new_hash(n):
    #生成100条hash，插入文件
    for i in range(0,1000):
        o=union()
        hash=o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt","thread_rw")
        print(hash)

    duration = datetime.now() - start
    print("duration:",duration)



def many_thread(n):
    # start = datetime.now()
    print("start:",start)
    threads = []
    for _ in range(n):  # 循环创建500个线程   n个线程每个循环m次
        t = threading.Thread(target=new_hash, args=(n,))  #execute_func 创建线程          t = threading.Thread(target=execute_func, args=[3])
        # t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
        threads.append(t)  #添加线程到线程组
    # print("threads",threads)  #Thread-5
    for t in threads:
        t.start()  #开启线程
    for t in threads:
        t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
    print('主线程结束了！' , threading.current_thread().name)
    duration = datetime.now() - start
    print("duration:",duration)
    #
if __name__ == '__main__':
    pass
    new_hash(1)
    # many_thread(1)  #明显提升 duration: 0:00:00.292179
    # many_thread(1000)  #明显提升 duration: 0:00:00.292179