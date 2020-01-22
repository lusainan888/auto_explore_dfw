# -*- coding: utf-8 -*-
# __author__ = 'lusn'

'''
1、登录
2、查询菜单
3、订餐
'''
import requests
import datetime
import time
import json
import re
import uuid
import threading
from http import cookiejar
from urllib import request,parse,error

class dinner():
    def __init__(self,name="13818071450"):          #       ,depart_id='168',user_id='604'
        # print("0")
        # self.Content-Type="application/x-www-form-urlencoded; charset=utf-8"
        self.headers={"Origin":"http://oa.dfgroup.pro:10000",
                     "Content-Type":"application/x-www-form-urlencoded; charset=utf-8"}
        self.Origin="http://oa.dfgroup.pro:10000"
        self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; ' \
                       'Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; ' \
                       'EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        self.bid="博风米饭"
        self.name=name
        self.now=int(round(time.time() * 1000))
        # self.depart_id=depart_id
        #self.user_id=user_id
    def login(self,name,password):
        # print("1")
        url="http://oa.dfgroup.pro:10000/api/hrm/login/checkLogin"
        data='islanguid=7&loginid=%s&userpassword=%s' \
             '&dynamicPassword=&tokenAuthKey=&validatecode=&' \
             'validateCodeKey=&logintype=1&messages=&isie=false&'%(name,password)
        # self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; ' \
        #                        'Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        # print(self.headers)
        r = requests.post(url=url,data=data,headers=self.headers)
        #print("登录后响应",r.status_code)
        # print(r.text)
        # d=json.loads(r.text)
        # print(d)

    def query_user_id(self):
        now=self.now
        url='http://oa.dfgroup.pro:10000/api/ec/dev/app/getUserInfo?__random__=%s'%(now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        r = requests.get(url=url,headers=self.headers)
        #print('query_user_id响应',r.status_code,r.text)
        d=json.loads(r.text)
        user_id=d['userid']
        # print(user_id)
        return user_id

    def id_datas(self):
        self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        url='http://oa.dfgroup.pro:10000/api/hrm/search/getHrmSearchResult'
        data='tabkey=default_3&showAllLevel=1&virtualtype=&resourcename=%s&manager=&subcompany=&department=&telephone=&mobile=&mobilecall=&jobtitle=&'%(self.name)
        #print(self.name)
        r = requests.post(url=url,data=data.encode(),headers=self.headers)#data.encode()
        #r = requests.post(url=url,data=data,headers=self.headers)
        #print('query_datas响应',r.status_code,r.text)
        key=json.loads(r.text)['sessionkey']
        url='http://oa.dfgroup.pro:10000/api/ec/dev/table/datas'
        data='dataKey=%s&current=1&sortParams=[]'%(key)
        # print(data)
        r = requests.post(url=url,data=data,headers=self.headers)
        #print('query_datas响应',r.status_code,r.text)
        d=json.loads(r.text)
        # print(d['datas'])
        # print(d['datas'][0])
        user_id=d['datas'][0]['id']
        depart_id=d['datas'][0]['departmentid']
        # print(user_id,depart_id)
        return [user_id,depart_id]


    def query(self):
        # print("2")
        now=int(round(time.time() * 1000))
        url="http://oa.dfgroup.pro:10000/api/public/browser/data/161?" \
            "currenttime=%s&formmodefieldid=11972&" \
            "type=browser.caidan&min=1&max=10&pageSize=10&__random__=%s"%(now,now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'

        # print("请求头:",self.headers)
        r = requests.get(url=url,headers=self.headers)
        print('query菜单接扣响应',r.status_code)
        r.encoding = r.apparent_encoding
        d=json.loads(r.text)
        # print(d['datas'])
        # print(d['datas'][0])
        # print(d['datas'][0]['cd'])
        dict1={}
        dict2={}
        for i in range(len(d['datas'])):
            print('菜名',i,":",d['datas'][i]['cd'],"id:",d['datas'][i]['id'])
            # print('id',i,":",d['datas'][i]['id'])
        #     # id=d['datas'][i]['id']
        #     # cd=d['datas'][i]['cd']
        #     # dict1.update(id)
        #     # dict2.update(cd)
        # ##将cd、id组成新字典，再根据cd获取对应id
        # print(dict1)
        # print(dict2)
        #     # ret = re.match("博风米饭",d['datas'][i]['cd'])
        #     # if ret.group()=='博风米饭':
        #     #     print(d['datas'][i]['id'])

    def query2(self):
        # print("2")
        now=int(round(time.time() * 1000))
        url="http://oa.dfgroup.pro:10000/api/public/browser/data/161?" \
            "currenttime=%s&formmodefieldid=11972&" \
            "type=browser.caidan&min=1&max=10&pageSize=10&__random__=%s"%(now,now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'

        # print("请求头:",self.headers)
        r = requests.get(url=url,headers=self.headers)
        #print('query2菜单接扣响应',r.status_code)
        # r.encoding = r.apparent_encoding
        d=json.loads(r.text)  #将string转换为dict
        for i in range(len(d['datas'])):
            print('菜名',i,":",d['datas'][i]['cd'],"id:",d['datas'][i]['id'])
            # if d['datas'][i]['cd']=='博风米饭-香煎海东鲳':
            ####将菜名和id写入excel

            ret = re.match("米饭",d['datas'][i]['cd'])        #d['datas'][i]['cd']
            if ret:
                self.id=d['datas'][i]['id']
                print("???",self.id)


        '''
        # print(d['datas'])
        # print(d['datas'][0])
        # print(d['datas'][0]['cd'])
        dict1={}
        dict2={}
        for i in range(len(d['datas'])):
            print('菜名',i,":",d['datas'][i]['cd'],"id:",d['datas'][i]['id'])
            # id=d['datas'][i]['id']
            # cd=d['datas'][i]['cd']
        #     # dict1.update(id)
        #     # dict2.update(cd)
        # ##将cd、id组成新字典，再根据cd获取对应id
        # print(dict1)
        # print(dict2)
        #     # ret = re.match("博风米饭",d['datas'][i]['cd'])
        #     # if ret.group()=='博风米饭':
        #     #     print(d['datas'][i]['id'])
        '''

    def token(self):
        now=int(round(time.time() * 1000))
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        url="http://oa.dfgroup.pro:10000/api/cube/new/card/layoutBase?" \
            "type=1&modeId=11&formId=-223&_key=63g1e3&guid=card&" \
            "uuid=%s&modedatastatus=0&__random__=%s"%(suid,now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'

        # print("请求头:",self.headers)
        r = requests.get(url=url,headers=self.headers)
        # print('token接扣响应',r.status_code)
        d=json.loads(r.text)
        self.token=d['token']
        # print(self.token)

    def order(self):
        url="http://oa.dfgroup.pro:10000/api/cube/new/card/doSubmit"
        # id='561'  #菜
        id=input("input:")
        # user_id='604'
        # depart_id='168'
        # user_id=o.query_user_id()
        user_id=o.id_datas()[0]
        depart_id=o.id_datas()[1]
        # print(user_id,depart_id)
        #user_id=self.user_id
        # depart_id=self.depart_id

        key='2ztu3u'  #?i69qrr
        token=self.token
        print("order token:",token)
        date=datetime.date.today()
        now=time.strftime("%H:%M")
        data='billid=&type=1&modeId=11&formId=-223&_key=%s&guid=card&' \
             'token=%s&layoutid=36&isFormMode=1&' \
             'iscreate=1&src=submit&currentLayoutId=36&pageexpandid=225&' \
             'JSONStr={"field11972":"%s","field10458":"%s","field10456":"%s","field10457":"%s","field11032":"%s"}' \
             '&btntype=&issystemflag=1&oldmodedatastatus=0&'%(key,token,id,date,user_id,depart_id,now)
        # print(data)
        self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        # print(self.headers)
        r = requests.post(url=url,data=data,headers=self.headers)
        print("order响应",r.status_code,r.text)
        d=json.loads(r.text)
        print(d['billid'])  #提取响应的：billid
        # return d['billid']
        self.billid=d['billid']

    def order2(self):
        url="http://oa.dfgroup.pro:10000/api/cube/new/card/doSubmit"
        id=self.id
        user_id='604'
        depart_id='168'
        key='2ztu3u'  #key不校验
        token=self.token #UUID
        print("order token:",token)
        date=datetime.date.today()
        now=time.strftime("%H:%M")
        data='billid=&type=1&modeId=11&formId=-223&_key=%s&guid=card&' \
             'token=%s&layoutid=36&isFormMode=1&' \
             'iscreate=1&src=submit&currentLayoutId=36&pageexpandid=225&' \
             'JSONStr={"field11972":"%s","field10458":"%s","field10456":"%s","field10457":"%s","field11032":"%s"}' \
             '&btntype=&issystemflag=1&oldmodedatastatus=0&'%(key,token,id,date,user_id,depart_id,now)
        print(data)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        print(self.headers)
        r = requests.post(url=url,data=data,headers=self.headers)
        print("order响应",r.status_code,r.text)
        d=json.loads(r.text)
        print(d['billid'])  #提取响应的：billid
        self.billid=d['billid']

    def query_supper(self):
        #查看今日是否点餐
        now=self.now
        url='http://oa.dfgroup.pro:10000/api/cube/search/getList?' \
            'customid=7&_key=2ztu3u&guid=search&con_10458=0,,&con_10456=-5' \
            '&isNewTableSearch=1&displayType=&isTempSearch=&__random__=%s'%(now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        r = requests.get(url=url,headers=self.headers)
        #print('getList响应',r.status_code)
        d=json.loads(r.text)  #将string转换为dict
        date=datetime.date.today()
        # print(d['datas'],date)

        url="http://oa.dfgroup.pro:10000/api/ec/dev/table/datas"
        token=self.token #UUID
        date=datetime.date.today()
        data='dataKey=%s&current=1&sortParams=[]'%(d['datas'])
        #print(data)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        #print(self.headers)
        r = requests.post(url=url,data=data,headers=self.headers)
        print("查是否订餐:",r.status_code)
        d=json.loads(r.text)
        # print(d['datas'][0]['rq'],type(d['datas'][0]['rq']))  #str
        # print(date,type(date)) #'datetime.date'
        # print(type(str(date)))
        if d['datas'][0]['rq']==str(date):
            print("今日已订餐")
        else:
            print("尚未订餐!")

    def delete_order(self):
        billid=self.billid
        billid=input("input:")
        now=int(round(time.time() * 1000))
        url='http://oa.dfgroup.pro:10000/api/cube/expand/deleteData?' \
            'customid=7&_key=2ztu3u&guid=search&operate=DeleteAction&billids=%s' \
            '&pageexpandid=237&modeId=11&__random__=%s'%(billid,now)
        #self.headers["Cookie"]='JSESSIONID=aaa32fTF8P1WVdf37sm7w; ecology_JSessionId=aaa32fTF8P1WVdf37sm7w; Systemlanguid=7; loginidweaver=604; languageidweaver=7; loginuuids=604; EM_JSESSIONID=C39885FFCEB3915C68C6F177061C2019'
        r = requests.get(url=url,headers=self.headers)
        print('delete_order响应',r.status_code,r.text)

if __name__ == '__main__':
    # print('dinner')
    list=['陆赛男']
    for p in list:
        o=dinner(p)#部门id、用户id '13818071450'
        # mylogin=o.login('lusainan@dfgroup.pro','Lsn051221')

        mylogin=o.login('lusainan@dfgroup.pro','Lsn051221')#账号、密码、
        mytoken=o.token()
        # mydatas=o.id_datas() #user_id depart_id

        # myquery=o.query()
        # mydinner=o.order()  #key 和token 问题，点餐报：order响应 200 {"repeat":true}表单重复提交  手动输入菜单id
        # myuser_id=o.query_user_id() #user_id
        myquery=o.query2()    #get 5个线程？

        # for i in range(1):  #get循环5次
        #     i=i+1
        #     myquery=o.query2()
        #     print(i)
        mydinner=o.order() #固定选博风家的菜 o.order2()           ########input点单o.order
        # time.sleep(2)
        myquerysupper=o.query_supper()  #是否点餐
        # time.sleep(2)
        # mydelete=o.delete_order()#取消订餐


