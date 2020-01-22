#coding=utf-8
from coingame.beans.create_data import CreateSoccerMockData
from coingame.config.globalparam import get_testEv
from coingame.module.gamePublicLogic import GamePublicRequest

from coingame.beans.myunittest import MyTest
import re
from public.common.util import get_all_files_in_local_dir, logger, SSH_Util
from coingame.config.globalparam import get_project_path, get_data_path, get_service_path
import time


class MockData(MyTest):

    o = GamePublicRequest()

    def _create_base_data(self):
        """创建基础数据(目录树  队伍名称)"""
        self.o.login_and_register.login()
        for case_obj in self.o.create_lsports_mock_data_obj.case_ls:
            case_obj = case_obj[0]
            self.o.crm.create_categories(case_obj.league,case_obj.sport_type)
            self.o.crm.add_or_edit(sport_type=case_obj.sport_type)

    def test_mock_data(self):
        logger.info('开始运行：创建 lsports mock_data')
        # self._create_base_data()
        self.o.create_lsports_mock_data_obj.create_match()

        pass