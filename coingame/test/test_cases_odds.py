#coding=utf-8
from coingame.beans.create_data import CreateSoccerMockData
from coingame.config.globalparam import get_testEv
from coingame.logic.odds_script import OddsStepScript
from coingame.module.gamePublicLogic import GamePublicRequest

from coingame.beans.myunittest import MyTest
import re
from public.common.util import get_all_files_in_local_dir, logger, SSH_Util
from coingame.config.globalparam import get_project_path, get_data_path, get_service_path
import time
from coingame.beans import public_values as w_p_v
from ddt import ddt, data, unpack
from coingame.beans.readCaseInfo import ReadRunCaseData

@ddt
class TestOdds(MyTest):
    """测试动态赔付"""

    case  = ReadRunCaseData('test_odds_cases.xlsx')
    o = OddsStepScript()
    testName = ''


    @data(*case.get_cases())
    @unpack
    def test_odds(self,case_obj):
        self.testName = case_obj.case_description
        logger.info('开始测试用例：'+self.testName)
        self.o.set_case_data(self.case,case_obj)

        script = getattr(self.o,case_obj.script_fun)
        script()


