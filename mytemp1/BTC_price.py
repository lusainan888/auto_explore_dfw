# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import requests
import json
import time
from datetime import datetime
#常用交易所行情
def third_usdt_price():
    url='https://www.alphavantage.co/query?' \
        'function=CURRENCY_EXCHANGE_RATE&from_currency=%s&to_currency=%s&apikey=%s'%("ETC","USDT","PP0XZ09T6D0HXQ3L")
    r=requests.get(url)
    print(r.text)
#1、指数游戏行情接口
class BTC_USDT_Price():
    def huobi(self):       #火币1
        url="https://api.huobi.pro/market/detail/merged?symbol=btcusdt"
        # url="https://api.huobi.pro/market/detail/merged?symbol=etcusdt"
        r = requests.get(url)
        # print(r.text)
        #json.loads将json格式数据转换为字典/json.dumps()函数是将字典转化为字符串
        r=json.loads(r.text)
        price=r['tick']['close']
        print ("BTC_1_price is: %s" %(price))
        # print (type(price))   #<class 'float'>
        return price

    def binance(self): #币安2
        url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['price']
        print ("BTC_2_price is: %s" %(price))
        return price

    def okex(self):  #OKex 3
        url="https://www.okex.com/api/index/v3/BTC-USD/constituents"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['data']['last']
        print ("BTC_3_price is: %s" %(price))
        return price

    def bitmex(self):#取卖价       #bitmex 4
        url="https://www.bitmex.com/api/v1/orderBook/L2?symbol=XBT&depth=1"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r[0]['price']
        print ("BTC_4_price is: %s" %(price))
        return price

    def bittrex(self):   #bittrex 5
        url="https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['result']['Last']
        print ("BTC_5_price is: %s" %(price))
        return price

    def zb(self):  #zb 6
        url="http://api.zb.cn/data/v1/ticker?market=btc_usdt"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['ticker']['last']
        print ("BTC_6_price is: %s" %(price))
        return price

    def bitstamp(self):#bitstamp 7
        url="https://www.bitstamp.net/api/v2/ticker/btcusd/"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['last']
        print ("BTC_7_price is: %s" %(price))
        return price

    def hitbtc(self):   #hitbtc  8
        url="https://api.hitbtc.com/api/2/public/ticker/btcusd"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['last']
        print ("BTC_8_price is: %s" %(price))
        return price

    def gateio(self):  #gateio  9
        url="https://data.gateio.co/api2/1/ticker/btc_usdt"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['last']
        print ("BTC_9_price is: %s" %(price))
        return price

    def fcoin(self):  #fcoin 10
        url="https://api.fcoin.com/v2/market/ticker/btcusdt"
        r = requests.get(url)
        # print(r.text)
        r=json.loads(r.text)
        price=r['data']['ticker'][0]
        print ("BTC_10_price is: %s" %(price))
        return price

    def no(self,no):
        if no==1:
            # self.huobi()
            return self.huobi()

        elif no==2:
            # self.binance()
            return self.binance()
        elif no==3:
            # self.okex()
            return self.okex()
        elif no==4:
            # self.bitmex()
            return self.bitmex()
        elif no==5:
            # self.bittrex()
            return self.bittrex()
        elif no==6:
            # self.zb()
            return self.zb()
        elif no==7:
            # self.bitstamp()
            return self.bitstamp()
        elif no==8:
            # self.hitbtc()
            return self.hitbtc()
        elif no==9:
            # self.gateio()
            return self.gateio()
        else:
            # self.fcoin()
            return self.fcoin()

    def extdata_getCoinAvgPrice(self):  #给指数游戏的三方接口
        # now = int(round(time.time()*1000))   #13位unix毫秒时间戳
        # print('now:',now)
        # now02 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
        # print("now2:",now02)  #转换为当前时间

        times=datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #当前时间
        # print (times)
        # 转为时间数组
        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
        # print(timeArray)
        # 转为时间戳
        timeStamp = int(time.mktime(timeArray))        #10位unix秒时间戳
        # print(timeStamp)

        # url="https://api-sp-inte1.dae.org/extdata/coin/getCoinAvgPrice?requestTime="+str(timeStamp)
        # url="https://api.coingame.com/extdata/coin/getCoinAvgPrice?requestTime="+str(timeStamp)
        url="https://testing-sp-api.dae.org/extdata/coin/getCoinAvgPrice?requestTime="+str(timeStamp)
        r = requests.get(url)
        print(r.text)
        r=json.loads(r.text)
        price=r['data']
        print ("avg_price is: %s" %(price))

class usdt_price():         #梁召usdt接口  NG
    def usdt(self):
        url="https://testing-sp-api.dae.org/quote-query/ticker_dtos"
        r = requests.get(url)
        print(r.text)

if __name__ == '__main__':
    third_usdt_price()
    # a=BTC_USDT_Price()
    # a.huobi()

    # a.no(4)         #输入不同no，查询不同交易所
    # a.extdata_getCoinAvgPrice()          #接口直接获取平均价格

    #
    # no=1
    # num = 0
    # num=float(num)
    # #
    # # for no in range(1,11):   ###[1,11）
    # #     s = a.no(no)
    # #     s=float(s)
    # #     # print(type(s))
    # #     no=no+1
    # #     num += s
    # # # print(num)
    # # # print(no)
    # # avg=num/(no-1)
    # # print("计算 avg is :%s" %(avg))
    #
    # # for i in range(10):
    # #     i=1
    #     a.extdata_getCoinAvgPrice()          #接口直接获取平均价格
    # #     i=i+1
    # a.huobi()          #OK
    # # a.binance()        #OK
    # # a.okex()           #OK
    # # a.bitmex()         #OK   失败概率高
    # # a.bittrex()        #OK
    # # a.zb()             #OK
    # # a.bitstamp()       #OK
    # # a.hitbtc()         #OK
    # # a.gateio()         #OK
    # # a.fcoin()          #OK

    # b=usdt_price()
    # b.usdt()
    #
    pass
