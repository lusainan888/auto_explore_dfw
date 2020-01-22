#__author__ = 'Dell'
#ETC
import decimal
import math
import numpy as np
import time
from web3 import Web3,HTTPProvider
def transaction(icon,isTx=False,newadd=False,npwd="123456"):
    if icon=="ETC":
        provider = Web3.HTTPProvider("http://172.17.1.111:8545")   #HTTPProvider连接结点  ETC
        web3 = Web3(provider)
        from_address='0x3198141741d4A34E1080AAEC46A982963aC73a69'  # ETC  162.8139384+1+2+3+0.2
        pwd="lusn123456"
        value=Web3.toWei(0.1, 'ether')
        #初始余额
        balance=web3.fromWei(web3.eth.getBalance(from_address),"ether")   #wei转换为ether  1.6953184
        print("ETC初始余额：",balance)   #161.639868

        if isTx==True:
            #解锁账号
            web3.personal.unlockAccount(from_address,pwd)
            #大小写 转换
            to_address=Web3.toChecksumAddress("0x65d05c3bd1588a377df9305a01d8476407fabcaa")

            #打币  以太币的最小单位为wei，1个eth相当于10的18次方wei  144.562052-0.2=143.3616264
            #当前钱包余额 33.2906907704158 ETC / 3 ETH /
            tx = web3.eth.sendTransaction({
                    'to': to_address,
                    'from':  from_address,
                    'value':value
                })
            txhash=Web3.toHex(tx)
            print("ETC txhash:",txhash)
        else:
            pass

    elif icon=="ETH":
        provider = Web3.HTTPProvider("http://172.17.1.112:8545")   #ETH
        web3 = Web3(provider)
        from_address='0x571BDc851AFC0B3C17baCf53e9cAAA204301CcdE'# ETH
        pwd="lusn123456"
        value=Web3.toWei(0.1, 'ether')
        # from_address='0x440eeF5E1bfaDDde83bdB6AAa91565909145Cec2'
        # pwd="123456"  #小号0.22643688ETH
        balance=web3.fromWei(web3.eth.getBalance(from_address),"ether")   #wei转换为ether
        print("ETH初始余额:",balance)
        if isTx==True:
            #解锁账号
            web3.personal.unlockAccount(from_address,pwd)
            #大小写 转换
            to_address=Web3.toChecksumAddress("0x440eeF5E1bfaDDde83bdB6AAa91565909145Cec2")
            tx = web3.eth.sendTransaction({
                    'to': to_address,
                    'from':  from_address,
                    'value': value
                })
            txhash=Web3.toHex(tx)
            print("ETH txhash:",txhash)

            # #交易查询：返回匹配指定交易哈希值的交易
            # result=web3.eth.getTransaction(txhash) #48.33315104
            # print("交易详情:",result)
        else:
            pass

    else:
        print("没有这个币种信息")

    if newadd==True:
        print(web3.personal.newAccount(npwd),npwd)#创建新地址
        #ETC 0x821d2eE4170a5545f9023fCF315AA4ba791a8DA8 lusn123456
        #ETC 0xAAB880032Ce78A0137c95DC27bE6B1f27fa186aE 123456

def change():
    value=0.1
    value=value*pow(10,18)
    print(value)
    np.set_printoptions(suppress=True)
    print (np.array(value))

if __name__ == '__main__':
    transaction("ETC",False,False)  #查询+不创建地址
    # transaction("ETH",True,False)   #交易+不创建地址
    # change()

