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
        # self.url="http://172.17.3.121:9091"  #内网  east-channel
        self.url="http://172.17.3.174:9091"  #内网  east-channel-new
        #self.url="http://180.167.14.226:9091"  #外网映射ip 2个ip都行
    #1、上链
    def post_up_unoin(self,hash,extraHash,isread=True):
        if isread==True:
            hash=o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt",info='rw')   #TRUE读TXT  False传参
        self.info=hash
        headers={"Content-Type":"application/json"}
        url=self.url+'/chain/file/create'
        #print(url)
        #print(url,type(hash))
        #data ='{"hash":"%s","extraHash":"%s"}' %(hash,extraHash)
        #print("hash:",hash)
        data ={"hash":hash,"extraHash":extraHash}
        data =json.dumps(data)  #dic-->str
        # data ='{"extraHash":"%s"}' %(extraHash) #1000 缺少参数
        # data ='{"hash":"%s"}' %(hash) #1000 缺少参数
        # data="{}"
        #print(data)
        start = datetime.now()
        # print("每次请求时间",start)
        r = requests.post(url=url,data=data,headers=headers)
        # print('up响应',r.status_code,r.text)
        #print('up响应',r.status_code,r.text,datetime.now())
        ####print('up响应',r.status_code,r.text,datetime.now())
        start1 = datetime.now()
        # print("每次响应时间",start1)
        duration = datetime.now() - start  #0:00:01.000333  1s
        ####print("上链需要时间:",duration)
        d=json.loads(r.text)  #字符串转化为字典
        print("上链message:",d["message"])
        # print("timestamp:",d["data"]["timestamp"])
        #
        # info=json.dumps(r.text) #将字典转化为字符串
        # print ("info",info)
        # self.info=info
        # ###print("info000",info)

        # ##将成功上链hash写入txt
        if d["message"]=='SUCCESS':
            union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\hashused.txt",info=self.info)
        #union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\file3.txt",info=info)
        self.hash=hash
    #2、查询
    def query_union(self,hash,isread=True):
        if isread==True:
            hash=self.hash
        #print("query:",hash)
        headers={"Content-Type":"text/xml"}
        url=self.url+'/chain/file/query?hash=%s'%(hash)
        # url=self.url+'/chain/file/query?hash='
        print(url,type(hash))
        start = datetime.now()
        r = requests.get(url=url,headers=headers)
        # print('query接扣响应:',r.text)
        #print('query接扣响应',r.status_code,"r.text",'我是一个线程函数:', datetime.now())
        # duration = datetime.now() - start
        # print("duration查询:",duration)
        # print(type(r.text))  #<class 'str'>
        # info=json.dumps(r.text)   # 是将dict(字典类型对象)转化成 str(字符串类型)
        #print(type(info))  #<class 'str'>
        # info=r.text
        #self.info=info
        d=json.loads(r.text)
        print("查询message:",d["message"])
        #union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\file1.txt",info=info)
        #union.read_write_info(self,"D:\\auto_test_nancy\\dfw_union\\data\\file2.txt",info=info)


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

        elif info=="thread_rw":
            fp = open(file_path,'r',encoding='utf8')    #读取，每次读取txt新值，再+1存入txt，下次利用
            s = fp.read()
            text = int(s)
            # f.close()
            f = open(file_path,'w')
            f.write(str(text+1))
            # f.close()
            file_hash=sha256hex(s)
            file_hash=f
            # return str(hash)
            return file_hash

        elif info=="w":
            fp = open(file_path,'w',encoding='utf8')  #写 info
            fp.write(self.info+"\n")

        else:
            # self.info=hash   ##写入新的hash用
            # print("这次是这里运行")
            #fp = open(file_path,'w',encoding='utf8')
            fp = open(file_path,'a+',encoding='utf8')  #写 info
            fp.write(info+"\n")
            # fp.write(self.info+"\n")

        fp.close()

    def execute_func(self,m):
        for _ in range(m):
            union.post_up_unoin(self,hash,extraHash)  #上链
            #union.query_union(self,hash)  #查询

    def many_thread(self,n,m):
        #定义n线程，循环m次
        start = datetime.now()
        print("start:",start)
        threads = []
        for _ in range(n):  # 循环创建500个线程   5个线程每个循环3次
            t = threading.Thread(target=union.execute_func,args=(self,m,))  #execute_func 创建线程
            threads.append(t)  #添加线程到线程组
            #t.setDaemon(True) # 给每个子线程添加守护线程  不重要线程才会加
        for t in threads:
            t.start()  #开启线程
        for t in threads:
            t.join()   #保证主线程等待全部子线程结束，自身才结束(使主线程阻塞，直到该线程结束)
        print('主线程结束了！' , threading.current_thread().name)
        duration = datetime.now() - start
        print("duration:",duration)

    def new_hash(self):
        #生成100条hash，插入文件C:\software\apache-jmeter-4.0\bin\lsn\demo\newhashused.txt
        for i in range(0,200):  #False 传
            hash=sha256hex("东方新闻news2"+str(i))
            self.info=hash
            union.read_write_info(self,"C:\\software\\apache-jmeter-4.0\\bin\\lsn\\script\\newhash1.txt",info=self.info)
        print("全新hash 100条生成完毕！！")
if __name__ == '__main__':
    o=union()
    start=datetime.now()
    print("开始时间：",datetime.now())
    # #生成100条hash
    o.new_hash()
    #单线程
    #
    # #1、上链、查询--传参False/读取文件True
    # hash=sha256hex("东方201新闻0002")
    # extraHash=sha256hex("999")
    # print(hash,extraHash)
    # o.post_up_unoin(hash,extraHash,True) #上链  调用一次2                 duration: 0:00:02.085866  TRUE读txt，False传参
    # # time.sleep(1)
    # #o.query_union(hash,False) #查询   调用一次 30ms                             duration: 0:00:00.036902  0.03S=30ms   TRUE取刚刚上链的hash,False传参

    #
    # #2、上链、查询--循环
    #for i in range(3):   #True  读取
    # for i in range(1):  #False 传参
    #     hash=sha256hex("东方301新闻"+str(i))
    #     extraHash=sha256hex("999")
    #     o.post_up_unoin(hash,extraHash,True) #上链  调用一次2                 duration: 0:00:02.085866  TRUE读txt，False传参
    # #     time.sleep(1)
    # #     o.query_union(hash,True) #查询   调用一次 30ms                             duration: 0:00:00.036902  0.03S=30ms   TRUE取刚刚上链的hash,False传参
    # #
    # #
    # pass

    print("结束时间：",datetime.now())
    print("耗时：",datetime.now()-start)
    # hash=sha256hex("东方401新闻")
    # extraHash=sha256hex("999")
    # o.query_union(hash,False) #查询   调用一次 30ms

    #3、稳定性测试：略

    # hash="ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f70"#上链成功
    # extraHash="75c46ca0240bac9d1024730d47e1a93ce86786602986bf1efc87fb9692cc6ff3"

    # i=37
    # hash=sha256hex("东方201新闻"+str(i))
    # extraHash=sha256hex("999")
    # o.query_union(hash) #查询   调用一次   duration: 0:00:00.036902  0.03S=30ms  9没上链
    # o.post_up_unoin(hash,extraHash) #上链  调用一次2s  duration: 0:00:02.085866

    # o.many_thread(2,1)
    # o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\readtemp.txt",info='rw')

    # start=datetime.now()
    # for i in range(82,83):
    #     hash=sha256hex("东方001新闻"+str(i))
    #     extraHash=sha256hex("999")
    #
    # # # # o.many_thread(2,1,hash,extraHash)
    #     o.post_up_unoin(hash,extraHash) #上链  调用一次2s  duration: 0:00:02.085866

    #     print(hash)
    '''
    # hash="ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52" \
    #      "ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f5200119"
    o.post_up_unoin(hash,extraHash) #上链  调用一次2s  duration: 0:00:02.085866
    #hash='712b2eb8f272b5483343a3fae73a25a525c7d2c5f319838fa0b1ffd8e11891a2'
    # print(len(hash))
    # print(hash+'\n'+extraHash)
    # hash="847d98befb07cc9a4c8c3f1da1c8f21e34e3e4410503d42bda9872f79bda6a93"
    time.sleep(2)
    # o.query_union(hash) #查询   调用一次   duration: 0:00:00.036902  0.03S=30ms  9没上链
    # duration = datetime.now() - start
    # print("总时间",duration)
    '''
    # o.read_write_info("D:\\auto_test_nancy\\\dfw_union\\data\\file1.txt")
    #o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\file1.txt","hello")#读取
    '''
    start=datetime.now()
    for i in range(100):
        print(i)
        o.query_union(hash)
    duration = datetime.now() - start
    print(duration)
    '''

    #thread
    # #hash=sha256hex("东方新闻1")
    # for i in range(1,3):
    #     hash=sha256hex("东方201新闻"+str(i))
    # extraHash=sha256hex("999")
    # # #o.query_union(None)
    # # o.post_up_unoin(None,extraHash)
    # o.many_thread(2,1,hash,extraHash) #8s

    # #写入新的hash
    # for i in range(200,500):
    #     hash=sha256hex("东方101新闻"+str(i))
    #     extraHash=sha256hex("999")
    #     o.read_write_info("D:\\auto_test_nancy\\dfw_union\\data\\hash.txt","1")
# 1、
# {"hash":"None","extraHash":"None"}
# up响应 200 {"code":0,"message":"SUCCESS","data":{"extraHash":"None","hash":"None","timestamp":1577263521163,"txHash":"8b8c11a588959d7fbf3d30ef7d5215909dbfa6e471342864a506caf8013eaa00"}}
