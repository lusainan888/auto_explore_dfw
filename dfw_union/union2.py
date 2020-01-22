# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import requests
import json
import time
import threading
from datetime import datetime
from public.common.SHAtools import sha256hex
class union():
    def __init__(self):
        # self.url="http://172.17.3.121:9091"  #内网
        self.url="http://172.17.3.174:9091"  #内网
    #1、上链
    def post_up_unoin(self,hash='',extraHash='',isread=True):
        if isread==True:
            hash=o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt",info='rw')   #TRUE读TXT  False传参
        self.info=hash
        print(self.info)
        headers={"Content-Type":"application/json"}
        url=self.url+'/chain/file/create'
        data ='{"hash":"%s","extraHash":"%s"}' %(hash,extraHash)
        start1 = datetime.now()
        ##########print("每次请求now时间",start1)
        r = requests.post(url=url,data=data,headers=headers)
        d=json.loads(r.text)
        start2 = datetime.now()
        #print("每次响应now时间=========",start2)
        duration = start2 - start1  #0:00:01.000333  1s
        # print("上链需要时间:",duration)
        print("上链message:",d["message"])
        d=json.loads(r.text)
        # ##将成功上链hash写入txt
        if d["message"]=='SUCCESS':
            union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\hashused.txt",info=self.info)
        self.hash=hash

    #2、查询
    def query_union(self,hash='',isread=True):
        if isread==True:
            hash=self.hash
        headers={"Content-Type":"text/xml"}
        # hash=union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\hash.txt",info=None)
        # hash=hash[0]
        url=self.url+'/chain/file/query?hash=%s'%(hash)
        # print(url,type(hash))  #<class 'builtin_function_or_method'>  不传  上链了
        r = requests.get(url=url,headers=headers)
        d=json.loads(r.text)
        print("查询message:",d["message"])


    def read_write_info(self,file_path,info=None):
        """向文件写或读取信息"""
        if info==None:
            fp = open(file_path,'r',encoding='utf8')    #读 None
            return fp.read()

        elif info=="rw":
            fp = open(file_path,'r',encoding='utf8')    #读取，每次读取txt新值，再+1存入txt，下次利用
            s = fp.read()
            text = int(s)
            f = open(file_path,'w')
            f.write(str(text+1))
            file_hash=sha256hex(s)
            return file_hash
        else:
            fp = open(file_path,'a+',encoding='utf8')  #写 info
            fp.write(self.info+"\n")
        fp.close()

    def execute_func(self,m):
        for i in range(m):
            union.post_up_unoin(self,hash,extraHash,True)  #上链
            # union.query_union(self,hash)  #查询

    #def many_thread(self,n,m,hash,extraHash):
    def many_thread(self,n,m):
        start = datetime.now()
        threads = []
        for _ in range(n):  # 循环创建500个线程   5个线程每个循环3次
            t = threading.Thread(target=union.execute_func,args=(self,m))  #execute_func 创建线程
            threads.append(t)  #添加线程到线程组
            #t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
        for t in threads:
            t.start()  #开启线程
        for t in threads:
            t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
        print('主线程结束了！' , threading.current_thread().name)
        duration = datetime.now() - start
        print("Duration:",duration)

if __name__ == '__main__':
    o=union()
    #单线程
    # for i in range(1):  #False 传参
    #     hash=sha256hex("东方301新闻"+str(i))
    #     extraHash=sha256hex("999")
    #     o.post_up_unoin('',extraHash,True) #上链  调用一次2                 duration: 0:00:02.085866  TRUE读txt，False传参
    #     time.sleep(1)
    #     o.query_union(hash,True) #查询   调用一次 30ms                             duration: 0:00:00.036902  0.03S=30ms   TRUE取刚刚上链的hash,False传参
    #


    #多线程thread 这不是真正的多线程并发
    extraHash=sha256hex("999")
    o.many_thread(5,5)  #不省时间

