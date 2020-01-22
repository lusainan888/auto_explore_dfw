# -*- coding: utf-8 -*-

import sys
import re
# sys.path.append(re.sub('\\\coingame.*','',__file__))
sys.path.append(re.sub('/coingame.*','',__file__))

import unittest
from coingame.config.globalparam import get_project_path, get_send_emails
from coingame.config.globalparam import get_project_path
from coingame.test.test_cases import CoinGameTestCases
from coingame.test.test_cases_mock_data import MockData
from public.common.MyTestResult import _TestResult
from public.common import HTMLTestRunner
import os
import time
import re
import shutil
from public.common.util import send_email

def send_emails(result,report_name):
    """发送邮件"""
    path = get_project_path()
    if re.search('[A-Z]:.*',path) != None:
        # 发送邮件
        all_cases_count = result.success_count+result.failure_count+result.error_count
        subject = '自动化测试结果(全部用例数:%s  通过：%s  失败：%s  错误：%s)'\
                  %(all_cases_count,result.success_count,result.failure_count,result.error_count)
        receivers = get_send_emails()
        send_email(receivers=receivers,subject=subject,msg='http://172.17.2.156:9000/'+report_name)


def main002():
    # try:
    #     cmd = 'pip freeze > '+get_project_path()+'/requirements.txt'
    #     os.popen(cmd)
    # except:
    #     pass


    # 2、html报告文件路径
    report_name = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))+'.html'
    report_path = get_project_path()+ '/coingame/report/'

    report_abspath = report_path+ report_name

    # 3、打开一个文件，将result写入此file中
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'接口自动化测试报告',
                                           description=u'用例执行情况：')

    testunit=unittest.TestSuite()

    allcase = get_project_path()+'/coingame/test/'
    loader = unittest.defaultTestLoader
    #使用discover找出用例文件夹下test_casea的所有用例
    discover=loader.discover(allcase,pattern='test_cases_mock_data.py')
    # discover=loader.discover(allcase,pattern='test_cases_odds.py')
    discover._tests.append(loader.discover(allcase,pattern='test_cases.py'))

    #使用for循环出suite,再循环出case
    for suite in discover:
        for case in suite:
            testunit.addTests(case)

    result = runner.run(testunit)

    fp.close()
    shutil.copy(report_abspath,report_path+'case_result.html')

    send_emails(result,report_name)


if __name__ == '__main__':
    # main002()
    s = '[{"odds":2.06,"optionAddress":"0x5982df6161d2b3353f73cb1d22d3258efd8178d2","optionId":29119},{"odds":2.87,"optionAddress":"0xb18551790208b7eb532786f0f52aee2da98271f5","optionId":29136},{"odds":2.91,"optionAddress":"0x0effe693296846cc99c5ef4128c0567497dc9c24","optionId":29153}]'
    s = '[{"optionId":29119,"optionAddress":"0x5982df6161d2b3353f73cb1d22d3258efd8178d2","odds":2.18},{"optionId":29136,"optionAddress":"0xb18551790208b7eb532786f0f52aee2da98271f5","odds":3.07},{"optionId":29153,"optionAddress":"0x0effe693296846cc99c5ef4128c0567497dc9c24","odds":3.12}]'
    reg = '.*({.*?29119})({.*?29119[},].*?})'
    print(re.search(reg,s))

    pass



