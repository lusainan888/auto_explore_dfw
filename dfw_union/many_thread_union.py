# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import requests
import json
import time
import threading
from multiprocessing import Pool
from datetime import datetime
from public.common.SHAtools import sha256hex
import random

mutex = threading.Lock()  #创建锁
thread_local_obj = threading.local()
# count=0
class union():
    def __init__(self,env="inner"):
        if env=='inner':
            self.url="http://172.17.3.121:9091"  #内网   self.url="http://172.17.3.174:9091   121、174
        else:
            self.url="http://180.167.14.226:9091"  #外网映射ip 2个ip都行

    #1、上链
    def post_up_unoin(self,hash,extraHash,isread=True):
        if isread==True:
            hash=o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt",info='rw')   #TRUE读TXT  False传参
        else:
            t = time.time()
            hash=str(random.randint(0,99999999))+str(round(t * 1000))

        self.info=hash
        # print(self.info,datetime.now()) #============
        headers={"Content-Type":"application/json"}
        url=self.url+'/chain/file/create'
        # if mutex.acquire(1):
        data ={"hash":hash,"extraHash":extraHash}
        data =json.dumps(data)  #dic-->str
            # mutex.release()#释放锁
        r = requests.post(url=url,data=data,headers=headers)
        d=json.loads(r.text)  #字符串转化为字典
        # print("上链message:",d["message"])
        rehash=d["data"]["hash"]
        # # print(hash,rehash)
        if hash==rehash:
            pass
            # print("请求响应一致")
        else:
            print("数据串了")
        #print("上链message:",d["message"],datetime.now())

        # ##将成功上链hash写入txt
        # if d["message"]=='SUCCESS':
        #     union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\hashused.txt",info=self.info)
        # #union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\file3.txt",info=info)
        # self.hash=hash
        # global count
        # count=count+1

    #2、查询
    def query_union(self,hash,isread=True):
        if isread==True:
            lines=union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\hashused.txt",info=None)
            hash=lines[0].replace('\n','')
        headers={"Content-Type":"text/xml"}
        url=self.url+'/chain/file/query?hash=%s'%(hash)
        # if mutex.acquire(1):   #获取锁
        r = requests.get(url=url,headers=headers)
        d=json.loads(r.text)  #字符串转化为字典
        print("查询message:",d["message"],datetime.now())
            # mutex.release()#释放锁

    def read_write_info(self,file_path,info=None):
        """向文件写或读取信息"""
        if info==None:
            fp = open(file_path,'r',encoding='utf8')    #读 None
            # return fp.read()
            return fp.readlines()
        elif info=="rw":
            if mutex.acquire(1):   #获取锁
                fp = open(file_path,'r',encoding='utf8')    #读取，每次读取txt新值，再+1存入txt，下次利用
                s = fp.read()
                text = int(s)
                f = open(file_path,'w')
                f.write(str(text+1))
                file_hash=sha256hex(s)
                mutex.release()#释放锁
                return file_hash

        else:
            fp = open(file_path,'a+',encoding='utf8')  #写 info
            fp.write(self.info+"\n")
        fp.close()
    def execute_func(self,m,choice=True,isread=True):
        for _ in range(m):
            if choice==True:
                union.post_up_unoin(self,hash,extraHash,isread)  #上链
                # print("1")
            else:
                union.query_union(self,hash,isread)  #查询
                # print("2")

    def many_thread_lock(self,n,m,choice,isread):
        #定义n线程，循环m次
        start = datetime.now()
        print("start:",start)
        threads = []
        for _ in range(n):  # 循环创建500个线程   5个线程每个循环3次
            t = threading.Thread(target=union.execute_func,args=(self,m,choice,isread))  #execute_func 创建线程
            threads.append(t)  #添加线程到线程组
            #t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
        for t in threads:
            t.start()  #开启线程
        for t in threads:
            t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
        print('主线程结束了！' , threading.current_thread().name)
        duration = datetime.now() - start
        print("duration:",duration)
        # print(count)

if __name__ == '__main__':
    o=union()
    hash=sha256hex("东方新闻1")
    hash="fd6261b74d3085d504e601443a8c0dbad60ecc60a4ba8eb0553b80f7dba9f7a5"
    extraHash=sha256hex("999")
    #True 上链  False查询 ;True读取，False传参
    o.many_thread_lock(10,10,True,False)  #lock() 加阻塞
    # o.many_thread_lock(10,1,True,True)   #读取文件单线程,阻塞了  有点问题 lock上


