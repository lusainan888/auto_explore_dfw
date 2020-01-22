#coding=utf-8
import random
import requests
from coingame.config.globalparam import get_project_path
import json
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.testEnvironmentManager1 import TestEnvironment
import time
from coingame.module.gamePublicLogic import GamePublicRequest
from public.common.util import add_sub_date
from coingame.beans import public_values as w_v


def connect_MQ():
    url = 'http://172.17.2.103:15672/api/whoami'
    headers={'Authorization':'Basic Z3Vlc3Q6Z3Vlc3Q='}
    session = requests.Session()
    # r = session.get(url=url,headers=headers)
    # print(r.text)

    url = 'http://172.17.2.103:15672/api/exchanges/%2F/amq.default/publish'
    params = '{"vhost":"/","name":"amq.default","properties":{"delivery_mode":1,"headers":{}},"routing_key":"lsports_mq_abtest","delivery_mode":"1","payload":"232","headers":{},"props":{},"payload_encoding":"string"}'
    # headers['Content-Type']='text/plain;charset=UTF-8'
    cookie={'auth':'Z3Vlc3Q6Z3Vlc3Q%3D'}

    r = session.post(url=url,headers=headers,data=params,cookies=cookie)

    print(r.text)

def test001():
    lsports_template = get_project_path()+'/coingame/data/coingame' \
                    '/interface_template_data/lsports_mq_template.json'
    d = json.load(open(lsports_template,encoding='utf-8'))
    print(d['Header'])


class Lsports():

    def __init__(self,domain='api.intranet.etcgame.com',testEv='testing'):
        self.test_ev = testEv
        lsports_template = get_project_path()+'/coingame/data/coingame' \
                    '/interface_template_data/lsports_mq_template.json'
        self.lsports_template_dict = json.load(open(lsports_template,encoding='utf-8'))
        self.events_ls = self.lsports_template_dict['Body']['Events'][0]
        fixture_dict = self.events_ls['Fixture']
        livescore_dict = self.events_ls['Livescore']
        self.markets_ls = self.events_ls['Markets']
        self.events_ls['Fixture'] = None
        self.events_ls['Livescore'] = None
        self.events_ls['Markets'] = None


        self.case  = ReadRunCaseData('lsports_data.xlsx')
        self.ev_obj = TestEnvironment(domain,testEv,isCrm=True)

    def test(self):
        """"""
        case_ls = self.case.get_cases()
        for case_obj in case_ls:
            case_obj = case_obj[0]
            self.lsports_template_dict['Header']['Type'] = case_obj.type
            sql = 'SELECT subscribe_odds from lsports_odds_subscribe ' \
                  'WHERE fixture_id=%s and market_id=%s'%(case_obj.fixtureId,case_obj.markets_id)
            db_result = self.ev_obj.db.public_query_info(sql)
            market_ls = json.loads(db_result[0][0],encoding='utf-8')
            for market in market_ls:
                price = float(market['Price'])
                # market['Price'] = price + 200
                market['Price'] = random.randint(1,7)
            self.events_ls['FixtureId'] = case_obj.fixtureId
            self.markets_ls[0]['Id'] = case_obj.markets_id
            self.markets_ls[0]['Name'] = case_obj.markets_name
            self.markets_ls[0]['Providers'][0]['Bets'] = market_ls
            self.events_ls['Markets'] = self.markets_ls
            # print(json.dumps(self.lsports_template_dict,ensure_ascii=False,indent=4))
            msg = json.dumps(self.lsports_template_dict,ensure_ascii=False)
            # print(msg)
            self.publish_mq(msg,self.test_ev)

    def publish_mq (self,msg,test_ev='testing'):
        """推送MQ"""
        print(msg)
        msg = msg.replace('"','\\"')

        session = requests.Session()
        headers={'Authorization':'Basic Z3Vlc3Q6Z3Vlc3Q='}

        url = 'http://172.17.2.103:15672/api/exchanges/%2F/amq.default/publish'
        params = '{"vhost":"/","name":"amq.default","properties":{"delivery_mode":1,"headers":{}},"routing_key":"lsports_mq_%s","delivery_mode":"1",' \
                 '"payload":"%s","headers":{},' \
                 '"props":{},"payload_encoding":"string"}'% (test_ev,msg)
        cookie={'auth':'Z3Vlc3Q6Z3Vlc3Q%3D'}

        r = session.post(url=url,headers=headers,data=params,cookies=cookie)

        print('推送消息后响应数据:',r.text)

def test_create_lsports_mock_data():
    o = GamePublicRequest()
    o.create_lsports_mock_data_obj.create_match()
    # index = o.create_lsports_mock_data_obj.read_participant_start_id()
    # print(index)

def test_add_or_edit():
    o = GamePublicRequest()
    o.login_and_register.login()
    o.crm.add_or_edit(sport_type=w_v.sport_tennis)
    # o.crm.dirtree_image_upload()
    # o.crm.create_categories(4,'网球')



import datetime
import re
if __name__ == '__main__':
    # lsports = Lsports()
    # lsports.test()
    test_create_lsports_mock_data()
    # test_add_or_edit()

    pass
