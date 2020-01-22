# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#=================面向对象==============
# post请求有两种请求格式：
# 1、key-value的格式'Content-Type':'application/x-www-form-urlencoded'
# 2、标准json的格式：'Content-Type':'application/json'

#        d=json.loads(r.text)   #字符串str转化为字典dict
#        d=json.dumps(a)        #字典dict转化为字符串str

import requests
import json
import time
import datetime
import os,sys


import requests
import csv
import time
import sys
import re
from requests_toolbelt import MultipartEncoder
from requests_toolbelt.auth.handler import AuthHandler

ev="pz"          #环境配置pz   testing
name="zhouyali"
categoryName="足球"
leagueName="法甲"
class GameLoginAndRegister():

    """登录 注册"""
    def __init__(self):
        '''
        self.testUrl="http://api.intranet.etcgame.com/%s"%(ev)      #api
        self.headers={"Origin": "http://"+ev+"-crm.intranet.etcgame.com"}
        self.Origin="http://%s-crm.intranet.etcgame.com"%(ev)          #Origin：https://testing-crm.cointest.link
        '''
        self.testUrl="https://api.shihutiandi.com/"      #api
        self.headers={"Origin": "https://crm.coingame.com"}
        self.Origin="https://crm.coingame.com"          #Origin：https://testing-crm.cointest.link
        # print("api:",self.testUrl)
        # print("headers:",self.headers)
        # print("Origin:",self.Origin)

    def login(self,name='shenjun',password='123456'):
        self.headers['Authorization']='Basic YnJvd3Nlcjo='  #添加单个字典元素
        self.headers['Content-Type']='application/x-www-form-urlencoded'
        # self.headers={'Authorization':'Basic YnJvd3Nlcjo='
        #             ,'Content-Type':'application/json;charset=UTF-8'}
        url=self.testUrl+'/uaa/oauth/token'
        param = 'username=%s&password=%s&scope=ui&grant_type=password'%(name,password)
        #print(url,param)
        r = requests.post(url=url,params=param,headers=self.headers)
        #print(self.headers)
        print('登录后响应',r.status_code)
        # print('登录后响应',r.text)   #uaa/oauth/token接口
        #print('登录后响应',"%s,%s" %(r.status_code,r.text))
        d=json.loads(r.text)   #字符串转化为字典
        # print("登陆响应字典:",d)
        # json.loads   json.dumps()函数是将字典转化为字符串  json.dump(写)和json.load(读)主要用来读写json文件函数
        self.headers['Authorization']='Bearer '+d['access_token']
        # print(self.headers)
        # return self.headers;


    def profile(self):
        '''登录后查询profile接口，获取登录的username，判断是否登录成功'''
        url=self.testUrl+'/profile'
        r = requests.get(url=url,headers=self.headers)
        print('profile接扣响应',r.status_code)
        # print('profile接口响应',"%s,%s" %(r.status_code,r.text))
        d=json.loads(r.text)             #字符串转化为字典 json.loads   json.dumps()函数是将字典转化为字符串  json.dump(写)和json.load(读)主要用来读写json文件函数
        print('你登录的用户名：',d['username'])
        username=d['username']
        if username==name:
            print("恭喜，登录成功。")
        else:
            print("抱歉，登录失败!")

    def register(self,username):
        #获取x-flow-id--->获取验证码--->输入注册信息,提交
        url=self.testUrl+'/flow/register'  #获取x-flow-id      1
        headers=self.headers
        r = requests.get(url=url,headers=headers)
        d=json.loads(r.text,encoding='utf-8')
        flowId=d["flowId"]
        # print('flowId',flowId)

        url = self.testUrl+"/vcode/register"   #获取验证码       2
        headers['x-flow-id']=flowId
        print(headers)
        data ='{"receiver":"%s"}' %(username)      #请求是个字符串       3
        r= requests.post(url, headers=headers,data=data)
        print ("验证码",r.text)

        url = self.testUrl+"/register"   #注册
        data ='{"marketingChannel":"","vcode":"123456","email":"%s","password":"12345678","autoLogin":true}'%(username)
        r= requests.post(url, headers=headers,data=data)
        #print(headers)
        print ("注册",r.status_code)
        print(r.text)





    def category(self):
        '''获取目录树'''
        url=self.testUrl+'/game-config/category'
        self.headers['Content-Type']='application/json'
        r = requests.get(url=url,headers=self.headers)
        # print('category接扣响应',r.status_code)
        # print('category接扣响应',"%s,%s" %(r.status_code,r.text))
        d=json.loads(r.text)  #字符串转化为字典
        #比如：获取足球 4
        for key in range(len(d)):
            # print(d[key]["categoryName"])
            if d[key]["categoryName"]==categoryName:
                # print(d[key]['categoryId'])
                return (d[key]['categoryId']);
        '''
        # dict={'a':'1','b':'2','c':'3'}
        # a=dict['b']
        # print(a)
        #
        # dic={'categoryId': 4, 'categoryName': '足球', 'sport': 'Soccer'}
        # print(dic['sport'])

        # i=3
        # dd=d[i]
        # print(dd)  #{'categoryId': 4, 'categoryName': '足球', 'sport': 'Soccer'}
        # ddd=d[i]['sport']
        # print(ddd) #Soccer
        '''

    def leagueId(self):
       #获取足球-法甲的leagueId 61
        '''获取leagueId'''
        categoryId=GameLoginAndRegister.category(self)
        # print(categoryId)
        url=self.testUrl+'/game-config/league/'+str(categoryId)
        # print(url)
        # print(self.headers)
        r = requests.get(url=url,headers=self.headers)
        # print('leagueId接扣响应',r.status_code)
        # print('leagueId接扣响应',"%s,%s" %(r.status_code,r.text))
        d=json.loads(r.text)  #字符串转化为字典
        # #比如：获取法甲 61
        for key in range(len(d)):
            # print(d[key]["categoryName"])
            if d[key]["leagueName"]==leagueName:
                # print(d[key]['leagueId'])
                return (d[key]['leagueId']);

    def gameconfiglist(self):
        #获取outeventId=id,time为比赛开始时间
        leagueId=GameLoginAndRegister.leagueId(self)
        url=self.testUrl+'/game-config/game/list?league='+str(leagueId)
        r = requests.get(url=url,headers=self.headers)
        # print('gameconfiglist接扣响应',r.status_code)
        d=json.loads(r.text)  #字符串转化为字典
        t = time.time()
        ms=int(round(t * 1000))    #毫秒级时间戳
        # print(ms)
        for key in range(len(d)):
            if d[key]["time"]>ms:
                # print(d[key]['time'],d[key]["id"])
                return (d[key]['time'],d[key]['id']);

    def gameconfig(self):                    #选择比赛1       条件:开始时间大于当前时间      #自建假比赛
        url=self.testUrl+'/game-config/game'
        self.headers['Content-Type']='application/json'
        # print(self.headers)
        leagueId=GameLoginAndRegister.leagueId(self)      #leagueId=61 法甲
        outeventId=GameLoginAndRegister.gameconfiglist(self)[1]       #outeventId=4615333
        time=GameLoginAndRegister.gameconfiglist(self) [0]        #time=1575139800000  开始时间
        # print(outeventId,time)
        closeTime=time
        param = '[{"defaultShrink":true,"etc":false,"defaultPlay":true,"eth":false,"eventId":%s,"leagueId":%s,"time":%s,"closeTime":%s}]'%(outeventId,leagueId,time,closeTime)
        print(param)

        r = requests.post(url=url,data=param,headers=self.headers)
        print(self.headers)
        print('game-config响应',r.text)

    def gameid(self):
        #获取比赛gamid 一般取最新的    预测发布--待提交
        url=self.testUrl+'/games/status/PENDING_SUBMISSION?useApi=true&pageNum=1&title='
        r = requests.get(url=url,headers=self.headers)
        # print('gameid接扣响应',r.status_code)
        d=json.loads(r.text)  #字符串转化为字典
        print(d["list"][0]["gameId"])  #第一个gameid
        return (d["list"][0]["gameId"]);

        # length=len(d)
        # length=len(d["list"])
        # print(length)

        # for key in range(len(d["list"])):  #range(20)=[0,20) 循环20次
        #     print(d["list"][key]["gameId"])
    def gameid_PENDING_REVIEW(self):
        #获取比赛gamid 一般取最新的    预测发布--待审核
        url=self.testUrl+'/games/status/PENDING_REVIEW?useApi=true&pageNum=1&title='
        r = requests.get(url=url,headers=self.headers)
        # print('gameid接扣响应-待审核',r.status_code)
        d=json.loads(r.text)  #字符串转化为字典
        print(d["list"][0]["gameId"])  #第一个gameid
        return (d["list"][0]["gameId"]);

    def gameid_PREDICTION(self):
        #获取比赛gamid 一般取最新的，状态=PREDICTION_PRE_LIVE/CLOSED    盘中管理IN_PREDICTION
        url=self.testUrl+'/games/status/PREDICTION_AND_CLOSED?categoryIds=&title=&pageNum=1'
        r = requests.get(url=url,headers=self.headers)
        # print('gameid接扣响应-盘中管理',r.status_code)
        d=json.loads(r.text)  #字符串转化为字典
        for i in range(len(d["list"])):
            if d["list"][i]["status"]=="PREDICTION_PRE_LIVE":
                print(d["list"][i]["gameId"])  #第一个gameid
                return (d["list"][i]["gameId"]);

    def playid(self):
        #获取一场比赛的所有playid
        gameid=GameLoginAndRegister.gameid(self)
        url=self.testUrl+'/games/publishing/%s/PENDING_SUBMISSION'%(gameid)
        r = requests.get(url=url,headers=self.headers)
        # print('playid接扣响应',r.status_code)
        d=json.loads(r.text)  #字符串转化为字典
        list=[]        #空列表
        for key in range(len(d["centringPlayInfoList"])):
            # print(d["centringPlayInfoList"][key]["playId"])
            a=d["centringPlayInfoList"][key]["playId"]
            # print(a)
            list.append(a)
        # print(list)      #playid组成的列表
        return list;

    def committed_plays(self):
        #提交比赛
        url=self.testUrl+'/games/publishing/committed_plays'
        #从txt读取json拼接成数组
        file = os.getcwd()+'/playid.txt'
        f = open(file,'r')
        body = f.read()
        # print("初始模板",body)  #读取txt中字典   str JSON元素使用双引号
        body=json.loads(body)  #将str转换为dict
        # print("初始模板",body)  #读取txt中字典   dict 字典元素使用单引号 {dict}
        temp =body   #{dict}
        gameid=GameLoginAndRegister.gameid(self)
        list=GameLoginAndRegister.playid(self)
        temp['gameId']=gameid
        # body['gameId']=gameid     #替换字典dict值
        body2=[]
        for i in range(len(list)):
        # for i in range(5):
            # body['basePlayId']=list[i]
            temp['basePlayId']=list[i]
            # print("temp:",temp)
            body2.append(temp)
        body2=json.dumps(body2)

            # file2 = os.getcwd()+'/playid2.txt'    #写入playid2.txt
            # f = open(file2,'w')
            # f.write(str(body))
            # f.close()
        print("最终模板",body2)
        r = requests.post(url=url,data=body2,headers=self.headers)
        print('committed_plays响应',r.status_code,r.text)
        f.close()
    def review_acception(self,gameid): #审核通过
        url=self.testUrl+'/games/review_acception'
        param='[%s]'%(gameid)
        r = requests.post(url=url,data=param,headers=self.headers)
        print("审核比赛接口响应:",r.status_code,r.text)

    def closed_plays(self,gameid): #封盘
        url=self.testUrl+'/games/prediction/closed_plays'
        #从txt读取json拼接成数组
        file = os.getcwd()+'/playid.txt'
        f = open(file,'r')
        body = f.read()
        body=json.loads(body)  #将str转换为dict
        temp =body   #{dict}
        # gameid=GameLoginAndRegister.gameid(self)
        list=GameLoginAndRegister.playid(self)
        temp['gameId']=gameid
        body2=[]
        for i in range(len(list)):
            temp['basePlayId']=list[i]
            body2.append(temp)
        body2=json.dumps(body2)
        print("最终模板",body2)
        r = requests.post(url=url,data=body2,headers=self.headers)
        print('closed_plays响应',r.status_code,r.text)
        f.close()

    def task_lists(self,eventId):  # fields名称里boundary   和   headers里的boundary一致
        m = MultipartEncoder(
            fields={'file': ('example.csv', open('example.csv', 'rb'), 'application/vnd.ms-excel'),
                    'taskListName': ("example.csv")
                    },
            boundary='----WebKitFormBoundarykhgDKtdBx1Ci8WBi'
        )
        self.headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundarykhgDKtdBx1Ci8WBi'
        url=self.testUrl+'/offline-events/'+eventId+'/task-lists'
        print(url)
        r = requests.post(url=url, data=m, headers=self.headers)
        print('批量打币成功',r.status_code,r.text)


#   def register(self,name):
#         self.headers['Content-Type']='application/json'
#         headers=self.headers
#         url=self.testUrl+'/flow/register'  #获取flowId({"Origin": XX,"Content-Type": "application/json"})
#         r= requests.get(url, headers=headers)
#         r_dict = json.loads(r.text,encoding='utf-8')  #json.loads函数的使用，将字符串转化为字典
#         flowId=r_dict["flowId"]
#
#         url=self.testUrl+'/vcode/register' #获取验证码
#         #self.headers['Content-Type']='application/json'
#         self.headers['x-flow-id']=flowId
#         #######print(self.headers)
#         param='{"receiver":"%s"}'%name
#         r= requests.post(url, headers=headers,data=param)
#
#         param ='{"marketingChannel":"","vcode":"123456","email":"%s","password":"12345678","autoLogin":true}'%(name)
#         url=self.testUrl+'/register'
#         # print(url)
#         # print(param)
#         r = requests.post(url=url,data=param,headers=headers)
#         #print(name,'注册后响应数据：',r.text)
#
#         #设置提币密码(调用登陆接口--获取Authorization--设置资金密码）
#         self.login(name,"12345678")
#         url=self.testUrl+'/profile/asset-password'
#         param='{"assetPassword":"123456"}'
#
#         r = requests.post(url=url,data=param,headers=headers)
#         #print(headers)
#         print('设置提币后的响应数据：',r.status_code)
#         print('设置提币后的响应数据：',r.text)
#
#
# class crm_activity():
#     '''登录后crm一切操作'''
#     def __init__(self):
#         self.testUrl="http://api.intranet.etcgame.com/%s"%(ev)
#         self.headers={"Origin": "http://"+ev+"-www.intranet.etcgame.com"}
#     def profile(self):
#         '''登录后查询profile接口，获取登录的username，判断是否登录成功'''
#         a=GameLoginAndRegister.login(self,name)
#         self.headers=a
#         # self.headers['Content-Type']='application/json;charset=UTF-8'
#         print(self.headers)
#         url=self.testUrl+'/profile'
#         r = requests.get(url=url,headers=self.headers)
#         # print('登录后响应',r.text)
#         print('profile接口响应',"%s,%s" %(r.status_code,r.text))
#         d=json.loads(r.text)             #字符串转化为字典 json.loads   json.dumps()函数是将字典转化为字符串  json.dump(写)和json.load(读)主要用来读写json文件函数
#         print('你登录的用户名：',d['username'])
#         username=d['username']
#         if username==name:
#             print("恭喜，登录成功。")
#         else:
#             print("抱歉，登录失败!")
#     def participant(self,sport):
#         '''lsport-队伍基础数据库'''
#         a=GameLoginAndRegister.login(self,name)
#         self.headers=a
#         self.headers['Content-Type']='application/json;charset=UTF-8'
#         url=self.testUrl+'/participant/getListByPage'
#         param = 'page=&size=1000&sport=%s&nameOrId=&range=0'%(sport)
#         r = requests.get(url=url,params=param,headers=self.headers)
#         print('participant响应',r.status_code)
#         # print('participant接口响应',"%s,%s" %(r.status_code,r.text))
#         d=json.loads(r.text)
#         # print (d)
#         '''
#         #获取字典key=content的value值    1
#         # print(d['content'])
#         #获取列表的第一个字段值
#         # print(d['content'][0])
#         '''
#         #获取字典的第一个participantId值
#         print(d["content"][0]["participantId"])
#         '''
#         #获取所有participantId值
#         list=[]
#         i=0
#         for i in range(len(d["content"])):
#             list.append(d["content"][i]["participantId"])
#             # print(d["content"][i]["participantId"])
#             i=i+1
#         print ("队伍第三方ID列表：",list)
#         '''

if __name__ == '__main__':
    pass
    o=GameLoginAndRegister()
    for i in range(1):  #get循环5次
        i=i+1
        o.login(name,'coingame666') #登陆-crm        #o.login()  #默认shenjun登陆
    o.profile()
    o.register('12121@qq.com')  #注册  (请求是个字符串、you
    # o.task_lists("2")  #打币工具
    # o.category()
    # o.leagueId()
    # o.gameconfiglist()
    # # o.gameid()
    # # o.gameid_PENDING_REVIEW()
    # o.gameid_PREDICTION()
    # o.playid()
    # o.gameconfig()    #新建比赛
    # o.committed_plays()  #提交比赛
    # o.review_acception(136157)   #审核比赛
    # o.closed_plays(136165)   #封盘
    # o.login('120@qq.com','12345678') #登陆-web
    # o.register('eee@qq.com') #注册

    # k=crm_activity()
    # k.profile()         #调用profile接口查询
    # k.participant("SOCCER") #足球SOCCER 篮球BASKETBALL  网球TENNIS  棒球BASEBALL 飞镖DARTS  斯诺克SNOOKER  队伍基础数据库

