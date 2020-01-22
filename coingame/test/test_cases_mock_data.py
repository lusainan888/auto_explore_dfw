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
    c = CreateSoccerMockData()
    o = GamePublicRequest()
    ssh = SSH_Util(testEv=get_testEv())


    def test_mock_data(self):
        logger.info('开始运行：创建 mock_data')

        self.testName = '创建 mock_data'
        self.c.create_upcoming_file()

        #上传文件
        dir = get_data_path()+'mock_data/'
        mock_files_ls = get_all_files_in_local_dir(dir)
        for file in mock_files_ls:
            name = file.replace(dir,'')
            self.ssh.up_or_down_file(file,'/opt/springfans/mock-service/%s'%name)
        time.sleep(300) #等待5min

    def test_register_users(self):
        logger.info('开始运行：创建 mock_data')
        self.testName = '注册用户'
        is_go_next_step = True
        for user_dict in self.c.register_users_dict_ls:
            result = self.o.login_and_register.register(user_dict)
            if result == False:
                #账号已存在  不用进行下一步操作
                is_go_next_step = False
                break

        if is_go_next_step:
            #修改acct_balance金额
            name_ls = ''
            for user_dict in self.c.register_users_dict_ls:
                name_ls += "'%s',"%user_dict['name']
            name_ls = re.sub(',$','',name_ls)
            self.o.db.update_acct_balance(name_ls)

            #  # 重启acct_service服务
            # shell = get_service_path('account-service','pz')
            # self.ssh.rum_cmd(shell)

        pass