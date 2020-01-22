from coingame.test.help_work import test001 as T
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.module.gamePublicLogic import GamePublicRequest
from coingame.beans import public_values as w_v
from public.common.publicUtil import MysqlUtil
from public.common.util import read_write_info, calculate_float_data

def test_temp_lsports():
    """测试用例"""
    # case  = ReadRunCaseData('testdata.xlsx')
    o = GamePublicRequest(http='https')

    for i in range(1):
        o.login_and_register.login()
        eventId = o.create_game_info.create_third_game_lsports(sport=w_v.sport_basktball,noneCenralCurrency_ls=[]
            ,league='',is_get_not_score_play=False)

        gameId = o.db.get_gameId(eventId['text'])
        o.game_bean.set_gameId(gameId=gameId)
        o.game_bean.submit_review()
        o.game_bean.pending_deployment_review()
        o.game_bean.deployment_review()
        o.game_bean.publish_review('PENDING_RELEASE')


def test001():
    """测试用例"""
    case  = ReadRunCaseData('testdata.xlsx')
    o = GamePublicRequest()
    case_ls = case.get_cases()
    for case_obj in case_ls:

        case_obj = case_obj[0]
        test_data_obj = case.get_test_data(case_obj.test_dataId)

        testName='(%s)%s'%(case_obj.caseId,case_obj.case_description)
        o.login_and_register.login()

        for i in range(1):

            gameId =613
            score = '2:1'
            o.game_bean.set_gameId(gameId=gameId)

            o.game_bean.close()
            o.game_bean.accept()

            # o.game_bean.set_game_score(score='0:5')
            # o.game_bean.fetch_game_amount(score='0:5')
            #
            # o.game_bean.save_win_option_check(win_index=0)

            o.game_bean.save_score_check(score=score)
            o.login_and_register.login('zhouyali')
            # o.game_bean.save_win_option_check(win_index=0)
            o.game_bean.save_score_check(score=score)

            o.game_bean.calc_award(score=score)

            # o.game_bean.fetch_game_amount(score='2:1')


            # o.award.set_berfore_award_users_acct_balance(gameId)
            # o.award.set_user_award_amount(gameId,o.game_bean.options_info_dict)
            # #s
            # o.award.set_after_award_users_acct_balance(gameId)
            # o.award.print_users_acct_balance_info()
            # o.award.check_users_cash()



import sys
import re
import os

if __name__ == '__main__':
    test_temp_lsports()     #建比赛
    # test_temp()
    # test001()          #开奖
    # temp()
    # inser_val()
    # print(os.environ)
    # d = {'a':1}
    # print(d.get('b',[]))
    # print(d)

    pass
