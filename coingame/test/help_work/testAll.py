#coding=utf-8
import websocket
from coingame.beans import public_values as p_v
from coingame.config import globalparam
from coingame.config.globalparam import get_project_path, get_data_path, get_service_path, get_send_emails
import os,sys
from public.common.util import get_all_files_in_local_dir, SSH_Util, send_email, search_str
import re
import shutil
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from coingame.beans import api_request_path_manager as api_m


def test001():
    # print(get_project_path())
    # db = coinGameDb()
    # print(db.get_gameId(61))
    # print(globalparam.get_testUrl())
    # e = TestEnvironment()
    # o = GameLoginAndRegister(e)
    # for k,v in o.__dict__.items():
    #     print(k,v)
    pass

def del_file(path,is_delete_all=False):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            if is_delete_all == True:
                del_file(c_path)
        else:
            os.remove(c_path)

def remove_files():
    path = get_project_path()+'/coingame/data/mock/'
    del_file(path)


def get_all_files_dirs():

    dir = get_data_path()+'mock_data/'
    ls = get_all_files_in_local_dir(dir)
    for l in ls:
        print(l)

def test_run_remote():
    ssh = SSH_Util('172.17.3.29','test','test')
    # ssh.up_or_down_file('E:/1.txt','/opt/springfans/mock-service/1.txt')
    dir = get_data_path()+'mock_data/'
    ls = get_all_files_in_local_dir(dir)
    for l in ls:
        # print(l.replace(dir,''))
        name = l.replace(dir,'')
        ssh.up_or_down_file(l,'/opt/springfans/mock-service/%s'%name)

def test_run_shell():
    shell = get_service_path('account-service','pz')
    ssh = SSH_Util('172.17.3.29','test','test')
    print(ssh.rum_cmd(shell))

def copy_file():
    source = 'E:/1.txt'
    shutil.copy(source,'E:/2.txt')

def sub_str():
    s = """
    ft1.1: Traceback (most recent call last): File "D:\lym\autotest\interfaceTest\coingame\beans\myunittest.py", line 37, in tearDown self.assertTrue(False,CASE_RESULT_TEXT)
    AssertionError: False is not true : (操作步骤：创建第三方数据比赛 )失败原因： league=123 已无比赛
    """
    print(re.search('False is not truefd :(.*)',s).group(1))


def test_send_email():
    sender = 'liyanmei@dae.org'
    receivers = ['905927335@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
    message['To'] =  Header("测试", 'utf-8')        # 接收者

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP('mail.dae.org')
        smtpObj.login(sender,'abcd1234')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")


def test_send_email001():
    # receivers = ['liyanmei@dae.org']
    receivers = get_send_emails()
    send_email(receivers=receivers,subject='测试主题',msg='测试内容000\n测试换行00')

def test003():
    base_dir = re.sub('/coingame.*','',__file__).replace('\\','/')
    print('abc',base_dir)
    print(get_project_path())


from decimal import Decimal

def test_re():
    s = '[{"odds":4.60,"optionAddress":"0x7826ca3283bb65c685591d7c74f272dafb32d586","optionId":4981},' \
        '{"odds":5.80,"optionAddress":"0x946da047d18361147b9e8bbed399d8c51265d5e7","optionId":4992}' \
        '{"odds":5.80,"optionAddress":"0x946da047d18361147b9e8bbed399d8c51265d5e7","optionId":4993}'

    a = re.search('.*({.*?4992})',s).group(1)
    reg = '.*({.*?4992})'
    a = search_str(reg,s,1)
    print(a)



class Person():
    """这里是类"""

    def __init__(self):
        self.name = 'test'
        self.pwd = '123456'

    def a001(self):
        """这里是类 方法"""

def f():
    """这里是f函数"""
    pass

def test_ws():
    header = ["Origin: http://abtest-www.intranet.etcgame.com"]

    origin='http://abtest-www.intranet.etcgame.com'
    ws = websocket.WebSocket()
    ws.connect('ws://api.intranet.etcgame.com/abtest/odds',origin=origin)
    print(type(ws))
    while True:
        result =  ws.recv()
        print("Received '%s'" % result)

if __name__ == '__main__':
    # test001()
    # print(p_v.PENDING_SUBMISSION)
    # remove_files()
    # get_all_files_dirs()
    # print(get_service_path('account-service','testing'))
    # test_run_remote()
    # test_run_shell()
    # copy_file()
    # sub_str()
    # test_send_email()
    # test_send_email001()
    # test003()
    # test_re()
    # p = Person()
    test_ws()
