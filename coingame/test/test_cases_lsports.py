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
from coingame.beans import public_values as w_v


@ddt
class CoinGameTestCases(MyTest):
    """测试开奖"""
    case  = ReadRunCaseData('testdata.xlsx')
    o = GamePublicRequest()
    testName = ''

    @data(*case.get_cases())
    @unpack
    def test_award(self,case_obj):
        """测试开奖"""
        test_data_obj = self.case.get_test_data(case_obj.test_dataId)

        self.testName='(%s)%s'%(case_obj.caseId,case_obj.case_description)
        logger.info('开始运行用例：(%s)%s'%(case_obj.caseId,case_obj.case_description))
        self.o.login_and_register.login()

        #创建栏目
        eventId = self.o.create_game_info.create_third_game(sport=w_v.sport_tennis,noneCenralCurrency_ls=[]
            ,league=test_data_obj.league,eventId=test_data_obj.event_id)
        # eventId = 872057
        gameId = self.o.get_gameIds(eventId['text'])
        self.o.game_bean.set_gameId(gameId=gameId)
        self.o.game_bean.submit_review()
        self.o.game_bean.pending_deployment_review()
        self.o.game_bean.deployment_review()
        self.o.game_bean.publish_review('PENDING_RELEASE')

        #投注
        self.o.users_betting(self.case.get_betting_params_and_users_dict(test_dataId=case_obj.test_dataId
                                            ,db = self.o.ev_obj.db,gameId=gameId,is_third_data=False))

        self.o.login_and_register.login()
        #封盘 审核通过
        self.o.game_bean.close()
        self.o.game_bean.accept()

        # # 开奖
        self.o.game_bean.set_game_score(test_data_obj.score)
        self.o.award.set_berfore_award_users_acct_balance(gameId)
        self.o.award.set_user_award_amount(gameId,self.o.game_bean.options_info_dict)
        self.o.game_bean.award()
        self.o.game_bean.accept()
        self.o.award.set_after_award_users_acct_balance(gameId)
        self.o.award.print_users_acct_balance_info()
        self.o.award.check_users_cash()

    # def test_modify_shrink(self):
    #     self.o.login_and_register.login()
    #     res = self.o.game_bean.modify_shrink(gameId=376,newValue=16)
    #     self.o.game_bean.accept(is_check_db=False)
        # print(res)







