# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import requests
import json
import time
import ddt
import os
import unittest
from base import  opera_excel
from operation_data import wirte_result,send_requests
from config import globalparam
#unittest+ddt 写测试用例
#测试用例用unittest框架组建，并用ddt数据驱动模式，批量执行用例

'''
1、从excel读取数据作为请求，封装requests请求
2、为不污染数据，生产excel_copy
3、测试结果写入excel_copy
'''
# 获取explore_union_case.xlsx路径
casepath=globalparam.get_case_path()
testxlsx = os.path.join(casepath, "explore_union_case.xlsx")


# 复制explore_union_case.xlsx文件到report下
# report_path = globalparam.get_report_path()
# reportxlsx = os.path.join(report_path, "result.xlsx")

report_path = globalparam.get_case_path()
reportxlsx = os.path.join(report_path, "explore_union_case_copy.xlsx")

testdata = opera_excel.ExcelUtil(testxlsx).dict_data()


@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        # 如果有登录的话，就在这里先登录了
        opera_excel.copy_excel(testxlsx, reportxlsx) # 复制xlsx
    @ddt.data(*testdata)
    def test_api(self, data):
        # 先复制excel数据到report
        res = send_requests(self.s, data)
        wirte_result(res, filename=reportxlsx)
        # 检查点 checkpoint
        check = data["checkpoint"]
        ##########print("检查点->：%s"%check)
        # 返回结果
        res_text = res["text"]
        ############print("返回实际结果->：%s"%res_text)
        # 断言  check点包含在返回值
        self.assertTrue(check in res_text)
if __name__ == "__main__":
    unittest.main()
