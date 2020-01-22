# -*- coding: utf-8 -*-
# __author__ = 'lusn'
'''
import requests
# url='https://api-sp-inte1.dae.org/game/getGameDnsInfo?keyName=channel'
# url='https://dns.dlcyjm.com/game/getGameDnsInfo?keyName=channel'
url='https://dns.rexingu.com/game/getGameDnsInfo?keyName=channel'
r = requests.get(url)
print (url)
print(r.text)
'''
 #多域名动态配置
import requests
def get_sso_url(env):
    if env=='intel':
        url='https://api-sp-inte1.dae.org/game/getGameDnsInfo?keyName=channel'

    elif env=='test':
        url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=channel'
        # print (url)

    elif env=='prd':
        # url='https://dns.dlcyjm.com/game/getGameDnsInfo?keyName=channel'
        url='https://dns.rexingu.com/game/getGameDnsInfo?keyName=channel'

    elif env=='gamename':   #keyName:文件名【游戏名+游戏id】
        # url='https://api-sp-inte1.dae.org/game/getGameDnsInfo?keyName=baccarat-03007'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=baccarat-03007'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=goal-02005'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=rocket-02002'
        url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=median-01003'
        url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=magnate-01004'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=index-01006'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=powerball-01008'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=mining-01001'

        # url='https://dns.dlcyjm.com/game/getGameDnsInfo?keyName=baccarat-03007'  #默认调用第一个
        # url='https://dns.rexingu.com/game/getGameDnsInfo?keyName=baccarat-03007' #如果不通则用第二个

    elif env=='coingame':
        url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=coingame.in'



    elif env=='android':
        url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=old_android'
        # url='https://testing-dns.asdy88.com/game/getGameDnsInfo?keyName=android'

    # header={'origin': 'www.coingame.in'}   #国内
    # header={'origin': 'www.coingame.com'}  #国外
    # r = requests.get(url,headers=header)
    r = requests.get(url)
    print(url)
    print(r.text)

if __name__ == '__main__':
    # a=get_sso_url('intel')
    a=get_sso_url('prd')
    # a=get_sso_url('prd')
    # a=get_sso_url('gamename')  #domain首页入口、cdn静态资源、sso接口域名、api接口wss  channelRecharge渠道充值提币界面  、domainRecharge主站充值提币界面 、serverApi 服务间调用api
    # a=get_sso_url('android')
    # a=get_sso_url('coingame')
