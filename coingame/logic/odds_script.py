#coding=utf-8

from coingame.beans.create_data import CreateSoccerMockData
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.globalparam import get_testEv
from coingame.module.gamePublicLogic import GamePublicRequest

from coingame.beans.myunittest import MyTest
import re
from public.common.util import get_all_files_in_local_dir, logger, SSH_Util
from coingame.config.globalparam import get_project_path, get_data_path, get_service_path
import time
from coingame.beans import public_values as w_p_v

class OddsStepScript():

    def __init__(self):
        self.o = GamePublicRequest()

    def check_betting_odds(self,gameId):
        """检查投注后动态赔率是否正确"""

        betting_users_and_params_dict = self.case.get_betting_params_and_users_dict(test_dataId=self.case_obj.test_dataId
                                            ,db = self.o.ev_obj.db,gameId=gameId
                                            ,sport_type='')
        betting_users_ls = betting_users_and_params_dict['users']
        betting_params_ls = betting_users_and_params_dict['betting_params']
        for user in betting_users_ls:
            userId = self.o.ev_obj.db.get_userId(user['user_name'])
            self.o.login_and_register.login(user['user_name'],user['user_password'])

            for params in betting_params_ls:
                params = '{"currency":"NULS","records":[{"currencyOptionId":209437,"odds":13.89,"amount":"1"}],"language":"zh"}'
                betting_result = self.o.website.betting(params,userId=user['user_name'])
                time.sleep(1)
                self.o.odds_obj.check_game_finally_odds(gameId)


    def set_case_data(self,case_data,case_obj):
        """设置测试用例数据
        case_data:ReadRunCaseData
        """
        self.case = case_data
        # self.case = ReadRunCaseData()
        self.case_obj = case_obj


    def test_soccer_odds(self):
        """测试足球动态赔付"""

        self.o.login_and_register.login()

        # #创建栏目
        # eventId = self.o.create_game_info.create_third_game(sport='Soccer'
        #                         ,noneCenralCurrency_ls=[])
        # gameId = self.o.get_gameIds(eventId['text'])
        gameId = 397
        self.o.game_bean.set_gameId(gameId=gameId)
        # #
        # self.o.game_bean.submit_review()
        # self.o.game_bean.pending_deployment_review()
        # self.o.game_bean.deployment_review()
        # self.o.game_bean.publish_review('PENDING_RELEASE')
        # #
        # # #检查最终赔率
        # self.o.odds_obj.check_game_finally_odds(gameId)
        # #
        # # #修改全部指定币种抽水
        # self.o.game_bean.modify_shrink(gameId,newValue='15',modify_currency=['ETC'])
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)
        # #
        # # # #修改全部币种抽水
        # self.o.game_bean.modify_shrink(gameId,newValue='10')
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)


        #投注
        # gameId =  436
        # self.check_betting_odds(gameId)

        for i in range(1):
            try:
                self.o.odds_obj.check_game_finally_odds(gameId)
                print('12')
            except:
                pass


        self.o.login_and_register.login()

        # #修改全部币种抽水
        self.o.game_bean.modify_shrink(gameId,newValue='10')
        self.o.game_bean.accept(is_check_db=False)
        self.o.odds_obj.check_game_finally_odds(gameId)




    def test_auto_funny_odds(self):
        """测试自定义趣味竞猜动态赔付"""

        self.o.login_and_register.login()
        # self.o.create_game_info.auto_create_funny(optionNum=int(self.case_obj.option_num)
        #                         ,noneCenralCurrency_ls=['ETC','ETH'])
        # gameId = self.o.get_gameIds(is_third=False,index=0)

        gameId = 321
        self.o.game_bean.set_gameId(gameId)

        # self.o.game_bean.submit_review()
        # self.o.game_bean.pending_deployment_review()
        # self.o.game_bean.deployment_review()
        # self.o.game_bean.publish_review('PENDING_RELEASE')
        #
        # # #检查最终赔率
        # self.o.odds_obj.check_game_finally_odds(gameId)
        #
        # #修改全部指定币种抽水
        # self.o.game_bean.modify_shrink(gameId,newValue='15',modify_currency=['ETC','ETH'])
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)
        #
        # # #修改全部币种抽水
        # self.o.game_bean.modify_shrink(gameId,newValue='10')
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)
        #
        #
        # #修改赔率
        # self.o.game_bean.modify_odds(newValue='3.1')
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)

        #投注
        # gameId =  436
        self.check_betting_odds(gameId)

        # self.o.login_and_register.login()
        #
        # # #修改全部币种抽水
        # self.o.game_bean.modify_shrink(gameId,newValue='10')
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)
        #
        #
        # #修改赔率
        # self.o.game_bean.modify_odds(newValue='3.1')
        # self.o.game_bean.accept(is_check_db=False)
        # self.o.odds_obj.check_game_finally_odds(gameId)

    def award(self):
        """开奖"""
        self.o.login_and_register.login()

        # self.o.create_game_info.auto_create_funny(optionNum=int(self.case_obj.option_num)
        #                         ,noneCenralCurrency_ls=[])
        # gameId = self.o.get_gameIds(is_third=False,index=0)

        gameIds = [53]
        for gameId in gameIds:
            self.o.game_bean.set_gameId(gameId)

            # self.o.game_bean.submit_review()
            # self.o.game_bean.pending_deployment_review()
            # self.o.game_bean.deployment_review()
            # self.o.game_bean.publish_review('PENDING_RELEASE')
            # #
            # self.check_betting_odds(gameId)
            #
            # self.o.login_and_register.login()

            # gameId = 456
            # self.o.game_bean.set_gameId(gameId)
            self.o.game_bean.close()
            self.o.game_bean.accept()
            self.o.game_bean.modify_award_option()
            self.o.game_bean.set_game_score('1:0')
            self.o.award.set_berfore_award_users_acct_balance(gameId)
            self.o.award.set_user_award_amount(gameId,self.o.game_bean.options_info_dict)
            self.o.game_bean.award()
            self.o.game_bean.accept()
            self.o.award.set_after_award_users_acct_balance(gameId)
            self.o.award.print_users_acct_balance_info()
            self.o.award.check_users_cash()



if __name__ == '__main__':
    pass


