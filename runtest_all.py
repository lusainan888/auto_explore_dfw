# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import unittest
import time
import re
from selenium import webdriver
#from HTMLTestRunner import HTMLTestRunner
from base.HTMLTestRunner_api import HTMLTestRunner
import os
from config import globalparam
curpath = os.path.dirname(os.path.realpath(__file__))
report_path = globalparam.get_report_path()
img_path = globalparam.get_img_path()
case_path = os.path.join(curpath, "operation_data")
# print(report_path,case_path)
def add_case(casepath=case_path, rule="operation_datas.py"):
    '''加载所有的测试用例'''
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule,)
    return discover

def run_case(all_case, reportpath=report_path):
    '''执行所有的用例, 并把结果写入测试报告'''
    now=time.strftime("%Y-%m-%d_%H%M%S")
    htmlreport = reportpath+now+r"result.html"
    print("测试报告生成地址：%s"% htmlreport)
    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner(stream=fp,
                           verbosity=2,
                           title=u"接口测试报告",
                           description="用例执行情况",
                          tester=u"Nancy Lu")  #测试人员名字，不传取默认

# stream　　　　保存文件路径
# title　　     　　标题
# description　　报告说明描述
# verbosity　　　测试结果的复杂程度，有三个值

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()

 #====查找最新的html测试报告文件
def new_file(test_dir):
    #列举test_dir目录下的所有文件，结果以列表形式返回。
    lists=os.listdir(test_dir)
    #sort按key的关键字进行排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间
    #最后对lists元素，按文件修改时间大小从小到大排序。
    lists.sort(key=lambda fn:os.path.getmtime(test_dir+'\\'+fn))
    #获取最新文件的绝对路径
    file_path=os.path.join(test_dir,lists[-1])
    #    L=file_path.split('\\')
    #    file_path='\\\\'.join(L)
    return file_path


def save_html_to_img():
    #将html报告截图保存指定路径
    driver = webdriver.Chrome()
    file_path=new_file(report_path)
    driver.get("file:///"+file_path)
    filename=file_path.split('/')[-1]
    filename=filename.replace("html","png")
    global img_path
    img_path=img_path+filename
    driver.get_screenshot_as_file(img_path)  #"D:\\explore_dfw\\data\\img\\1.png"
    driver.quit()

if __name__ == "__main__":
    #执行case
    cases = add_case()
    run_case(cases)

    #查找最新的report
    # new_file(report_path) #    new_file('D:\\explore_dfw\\data\\report')
    #
    # save_html_to_img()  #html报告截屏 最新的
