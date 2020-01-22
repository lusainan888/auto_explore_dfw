# -*- coding: utf-8 -*-
# __author__ = 'lusn'

import requests
from coingame.config.globalparam import get_project_path, get_testEv, get_testUrl,get_data_path
from coingame.module.db import coinGameDb
import re
from coingame.beans import public_values as w_v
import json
import copy

interface_data_path=get_project_path()+'/coingame/data/coingame/' #31、32行  或者1
# interface_data_path=get_data_path()+'coingame/'  #或者2
# print("data/coingame目录:",interface_data_path) #D:/auto_test_nancy/coingame/data/coingame/ 获取指定目录

class TestEnvironment():

    def __init__(self,domain=None,testEv=None,isCrm=True,http='http',is_pre=True):
        self.game_play_old_status = '' #玩法操作之前的状态
        self.game_play_new_status = '' #玩法操作之后的状态

        if domain == None:
            self.testEv = get_testEv()  #读取config.ini 默认的配置 [testEv]
            self.testUrl = get_testUrl() #读取config.ini 默认的配置 [testDomain]+[testEv]
        else:
            self.testEv=testEv   #要自己传参，不用默认的testEv=None
            self.testUrl='%s://%s/%s'%(http,domain,testEv)
        testEv = self.testEv
        if is_pre:
            self.testUrl = re.sub('/pre$','',self.testUrl)# self.testUrl中匹配到的删除  匹配规则:结尾是/pre就删掉
        self.invalid_league_file = interface_data_path+'invalid_league_ls.txt'
        self.invalid_eventId_file = interface_data_path+'invalid_eventId_ls.txt'

        print(self.testEv,self.testUrl)
        self.invalid_league_file = interface_data_path+'invalid_league_ls.txt'
        self.invalid_eventId_file = interface_data_path+'invalid_eventId_ls.txt'
        print(self.invalid_league_file,self.invalid_eventId_file)

        if self.testEv=='testing':
            self.db=coinGameDb(host='172.17.1.128',db='sp_test')
        elif self.testEv=='abtest':
            self.db=coinGameDb(db='sp_abtest')
        elif self.testEv=='demo':
            self.db=coinGameDb(db='sp_demo')
        elif self.testEv=='pz':
            self.db=coinGameDb(db='sp_pz_test')
        elif self.testEv=='beta':
            self.db=coinGameDb(host='172.17.3.163',db='sp_beta')
        else:
            self.db=coinGameDb(db='sp_test')

        if isCrm:
            self.Origin='%s://%s-crm.intranet.etcgame.com'%(http,testEv)
            if testEv == 'pre':
                self.Origin='%s://%s-crm.coingame.com'%(http,testEv)
        else:
            self.Origin='%s://%s-www.intranet.etcgame.com'%(http,testEv)
            if testEv == 'pre':
                self.Origin='%s://%s-www.coingame.com'%(http,testEv)
        self.session = requests.Session()
        self.headers = {'Authorization':'Basic YnJvd3Nlcjo=','Content-Type':'application/x-www-form-urlencoded','Origin':self.Origin}
        # self.headers = {'Authorization':'Basic YnJvd3Nlcjo=','Origin':self.Origin}

    def clear_attr(self):
        self.game_play_new_status = ''
        self.game_play_new_status = ''
        self.pre_run_step_name = '' #运行的前一个步骤
        # print("clear 后:",self.game_play_new_status)

    def public_send_request(self,request_name='',
                data=None,headers=None,params=None
                ,file_dict=None,content_type=None):

        if isinstance(params,dict):
            params = json.dumps(params,ensure_ascii=False)

        if headers == None:
            headers = copy.deepcopy(self.headers)


        if content_type != None:
            headers['Content-Type'] = content_type

        request_arr = request_name.split(',')
        url = self.testUrl + request_arr[0]
        request_type = request_arr[1]

        if file_dict != None:
            # headers['Content-Type'] = w_v.upimage_content_type
            headers.pop('Content-Type')
            return self.session.post(url,files=file_dict,headers=headers)


        # request_params_dict = {'url':url,'headers':headers,'files':file_dict}
        request_params_dict = {'url':url,'headers':headers}
        if params != None:
            request_params_dict.setdefault('params',params.encode())
        if data != None:
            try :
                request_params_dict.setdefault('data',data.encode())
            except:
                request_params_dict.setdefault('data',data)

        if request_type == 'post':
            return self.session.post(**request_params_dict)
        if request_type == 'get':
            return self.session.get(**request_params_dict)
        if request_type == 'put':
            return self.session.put(**request_params_dict)
        if request_type == 'options':
            return self.session.options(**request_params_dict)

if __name__=='__main__':
    #t=TestEnvironment(domain=None,testEv=None,isCrm=True,http='http',is_pre=True)
    t=TestEnvironment()  #全部默认
    # t=TestEnvironment("api.intranet.etcgame.com",'pz',"","","False")

    pass

