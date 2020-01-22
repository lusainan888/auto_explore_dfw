# -*- coding: utf-8 -*-
# __author__ = 'lusn'

import json
import requests
class explore():
    def __init__(self):
        self.url="http://172.17.3.187:8080"
        self.Origin="http://172.17.3.187:8080"
        self.headers={"Content-Type": "application/json"}
    def login(self):
        url=self.url+"/auth/login"
        headers=self.headers
        data='{"user":"admin","password":"%s","network":"first-network"}' %("adminpw")
                # param = 'username=%s&password=%s&scope=ui&grant_type=password'%(name,password)
        r = requests.post(url=url,data=data,headers=headers)
        #json.dumps()用于将字典形式的数据转化为字符串，json.loads()用于将字符串形式的数据转化为字典
        d=json.loads(r.text)
        self.headers['Authorization']='bearer'+' '+d['token']

    def get_info(self):
        url=self.url+"/api/channels/info"
        headers=self.headers
        r = requests.get(url=url,headers=headers)
        d=json.loads(r.text)
        #print("channelname=",d['channels'][0]['channelname'])
        print("blocks=",d['channels'][0]['blocks'])           #blocks
        print("transactions=",d['channels'][0]['transactions'])  #transactions
        self.get_channel_genesis_hash=d['channels'][0]['channel_genesis_hash']
        print('\n')
        #print("createdat=",d['channels'][0]['createdat'])

    def get_node(self):
        url=self.url+"/api/status/%s"%(self.get_channel_genesis_hash)
        headers=self.headers
        r = requests.get(url=url,headers=headers)
        d=json.loads(r.text)
        print("txCount=",d['txCount'])
        print("latestBlock=",d['latestBlock'])
        print("peerCount=",d['peerCount'])
        print("chaincodeCount=",d['chaincodeCount'])
        print('\n')

    def get_PeerName(self):
        url=self.url+"/api/peersStatus/%s"%(self.get_channel_genesis_hash)
        headers=self.headers
        r = requests.get(url=url,headers=headers)
        print(r.text)
        #将响应有效信息组成新的dictionary、
        print('\n')


if __name__ == '__main__':
    o=explore()
    o.login()
    # o.get_info()
    # o.get_node()
    # o.get_PeerName()
