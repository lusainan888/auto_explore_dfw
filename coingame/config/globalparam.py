#coding=utf-8


import os,sys
from public.common.publicUtil import ReadConfig
import re

# caseManagerName='allPageManager.xlsx'

# 读取配置文件 config.ini
config_file_path = os.path.split(os.path.realpath(__file__))[0] #当前执行目录
read_config = ReadConfig(os.path.join(config_file_path,'config.ini'))  #config.ini
# # 项目参数设置
# prj_path = read_config.getValue('projectConfig','project_path')

def get_testUrl():
    """获取测试环境"""
    url = read_config.getValue('testDomain','testDomain')
    testEv = read_config.getValue('testEv','testEv')
    return url + testEv

def get_testEv():
    """获取测试环境"""
    testEv = read_config.getValue('testEv','testEv')
    return  testEv


def get_project_path():
    """获取工程路径"""
    # project_name=read_config.getValue('projectNameConfig','project_name')
    # p = re.search('(.*?)%s'%(project_name), os.getcwd(), re.M|re.I)
    # prj_path = p.group(1)+project_name
    base_dir = re.sub('/coingame.*|\\\coingame.*','',__file__).replace('\\','/')
    return base_dir

def get_data_path():
    """获取数据存放路径"""
    return get_project_path()+'/coingame/data/'

def get_logfile_path():
    return get_project_path()+'/coingame/log/'


def get_service_path(service_name,testEv):
    name = '%sService'%testEv
    res = read_config.getValue(name,name)
    res = res.replace('service_name',service_name)
    return res

def get_testEv_ip_name_pwd(testEv):
    if testEv == 'pz':
        return {'ip':'172.17.3.29','name':'test001','pwd':'test1234'}
    return {'ip':'172.17.3.29','name':'test001','pwd':'test1234'}  #最后返回的都是这行


def get_send_emails():
    """获取需要发送邮件的邮箱"""
    emails = read_config.getValue('sendEmails','sendEmails').replace('\n','')
    return emails.split(',')

# def getEtcgameCaseInfo(getManagerFile=True):
#     """获取etcgame的用例信息 如果传入参数=True则获取工程用例管理文件 否则只获取用例的路径"""
#     if getManagerFile:
#         return os.path.join(prj_path,'data','etcgame',caseManagerName)
#     return os.path.join(prj_path,'data','etcgame\\')
#
#
# def getCaseDataPath(projectName):
#     return os.path.join(prj_path,'data',projectName+'\\')


if __name__=='__main__':
    # print(get_testUrl()) #url + testEv  完整url
    # print(get_testEv())
    print(get_project_path())  #D:/auto_test_nancy  工程项目路径
    print(get_data_path())     #data路径
    # print(get_logfile_path())  #log存放路径
    # print(get_service_path("image-service",get_testEv())) #执行deploy.sh服务启动服务
    # print(get_testEv_ip_name_pwd('pz'))  #这个返回的都是这个结果
    #print(get_send_emails())  #定义收件人
    pass

