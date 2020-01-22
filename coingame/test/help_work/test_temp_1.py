#coding=utf-8
from decimal import Decimal
from coingame.beans.coinGameBeans import OptionInfo
from coingame.beans.dataBean import BettingBean, UserAcctBalanceInfo
from coingame.beans.myunittest import MyTest,CASE_RESULT_TEXT
from coingame.beans import  myunittest
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.globalparam import get_project_path
from coingame.module.gamePublicLogic import GamePublicRequest
from public.common.util import OperatorExcel, logger
import re
import time
from ddt import ddt, data, unpack


@ddt
class CoinGameTestCases001(MyTest):
    """测试用例"""

    def test_001(self):
        self.testName='测试名称:新模块001'
        print('test_001_001')
        # self.assertTrue(True,'fail失败')
        self.assertTrue(False,'fail0000失败')

    def test_002(self):
        self.testName='测试名称:新模块002'
        print('test_001_002')
        # self.assertTrue(True,'fail失败')
        self.assertTrue(False,'fail0000失败')

    def test_003(self):
        self.testName='测试名称:新模块003'
        self.assertTrue(True,'fail失败')
        print('test_001_002')







