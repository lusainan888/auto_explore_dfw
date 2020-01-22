# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#封装get、post请求
import requests
import json
import xlrd
from openpyxl import load_workbook
import openpyxl
from io import StringIO
import sys
import time
import unittest
from base.opera_excel import ExcelUtil
from base.opera_excel import Write_excel
from base.opera_excel import copy_excel

class Webrequests():
    #封装POST
    def httpPost(self,url,data,header=None):
        res = None
        if header !=None:
            res=requests.post(url,data=data,headers=header)
        else:
            res = requests.post(url=url,data=data)
        return res

    #封装GET
    def httpGet(self,url,data,header=None):
        res = None
        if header !=None:
            res = requests.get(url=url,data=data,headers=header,verify=False)
        else:
            res = requests.get(url=url,data=data,verify=False)
        return res

    #封装Request
    def httpGetOrPost(self,method,url,data,header):
        if method in "get":
            mres=self.httpGet(url,data,header)
        elif method == "post":
            mres=self.httpPost(url,data,header)
        elif method in"put":
            mres=requests.put(url,data=data,headers=headers)
        elif method in "delete":
            mres=requests.delete(url,data=data,headers=headers)
        else:
            mres = requests.post(url, data=data, headers=headers)
            print("错误")
        return mres.json()

    #case1
    def test0001(self):
        self.url="http://172.17.3.187:8080/auth/login"
        self.method="post"
        self.data='{"user":"admin","password":"%s","network":"east-network"}' %("adminpw")
        self.header={"Content-Type": "application/json"}
        d=self.httpGetOrPost(self.method,self.url,self.data,self.header)
        if d["message"]=="You have successfully logged in!":
            print("登录 PASS")
        else:
            print('exception:',d["message"])


    #封装excel
    def readSheetdata(self,cell):
        wb=load_workbook(r'D:\auto_test_nancy\dfw_union\data\explore_union_case.xlsx')
        sheet=wb.active
        value=sheet[cell]
        print(value.value,type(value.value))
        return value.value

TestResult = unittest.TestResult
#美化HTML报告
class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.


    def __init__(self, stream='', descriptions='', verbosity=''):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.skipped_count=0#add skipped_count
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        #所有用例的结果 例:self.result.append((1, test, output, _exc_str,self.startTime,endTime))
        self.result = []


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.startTime=time.time()

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        endTime=time.time()
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        # self.result.append((0, test, output, '',self.startTime,endTime))
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addSkip(self, test, reason):
        self.skipped_count+= 1
        TestResult.addSkip(self, test,reason)
        output = self.complete_output()
        # self.result.append((3, test,'',reason))
        self.result.append((3, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('skip ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('s')

    def addError(self, test, err):
        endTime=time.time()
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        # self.result.append((2, test, output, _exc_str,self.startTime,endTime))
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        endTime=time.time()
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        # self.result.append((1, test, output, _exc_str,self.startTime,endTime))
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')




if __name__ == '__main__':
    a=Webrequests()
    a.test0001()
    a.readSheetdata("J2")  #Webrequests没用到   _TestResult被HTMLTestRunner.py调用


