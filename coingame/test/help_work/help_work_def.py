from coingame.test.help_work import test001 as T
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.module.gamePublicLogic import GamePublicRequest
from coingame.beans import public_values as w_v
from public.common.publicUtil import MysqlUtil
from public.common.util import read_write_info, calculate_float_data


def test001():
    T.global_dict['a'] = 100


def test_temp():
    """测试用例"""
    case  = ReadRunCaseData('testdata.xlsx')
    o = GamePublicRequest(http='https')
    case_ls = case.get_cases()
    for case_obj in case_ls:
        read_write_info(w_v.event_id_file,'{}')
        case_obj = case_obj[0]
        test_data_obj = case.get_test_data(case_obj.test_dataId)

        testName='(%s)%s'%(case_obj.caseId,case_obj.case_description)
        o.login_and_register.login()
        for i in range(1):
            o.login_and_register.login()
            # eventId = o.create_game_info.create_third_game_by_need(sport=w_v.sport_soccer,noneCenralCurrency_ls=[]
            #     ,is_get_not_score_play=False,case_data_obj=test_data_obj)
            # print(eventId)
            # o.create_game_info.auto_create_funny(optionNum=2
            #                     ,noneCenralCurrency_ls=[])
            # gameId = o.get_gameIds(is_third=False,index=0)

            # # # #创建栏目
            # eventId = o.create_game_info.create_third_game(sport=w_v.sport_soccer,noneCenralCurrency_ls=['ETC','ETH']
            #     ,league='',eventId='',is_get_not_score_play=False,case_data_obj=test_data_obj)
            # # eventId = 872057
            # gameId = o.db.get_gameId(eventId['text'])
            gameId = 588
            o.game_bean.set_gameId(gameId=gameId)
            o.game_bean.submit_review()
            o.game_bean.pending_deployment_review()
            o.game_bean.deployment_review()
            o.game_bean.publish_review('PENDING_RELEASE')
            #
            # gameId = 485
            # o.game_bean.set_gameId(gameId=gameId)
            # # #投注
            # o.users_betting(case.get_betting_params_and_users_dict(test_dataId=case_obj.test_dataId
            #                                     ,db = o.ev_obj.db,gameId=gameId,is_third_data=True,
            #                                     game_score=test_data_obj.score))
            #
            # o.login_and_register.login()
            #
            #
            # gameId = 431
            # o.game_bean.set_gameId(gameId=gameId)
            # #
            # #  #封盘 审核通过
            # o.game_bean.close()
            # o.game_bean.accept()
            # #
            # # # o.game_bean.modify_award_option()
            # # # o.game_bean.set_game_score(score='2:1')
            # # # o.game_bean.fetch_game_amount(score='2:1')
            # #
            # # #开奖
            # # # o.game_bean.modify_award_option()
            # o.game_bean.set_game_score(score='0:5')
            # o.game_bean.fetch_game_amount(score='0:5')
            # o.award.set_berfore_award_users_acct_balance(gameId)
            # o.award.set_user_award_amount(gameId,o.game_bean.options_info_dict)
            # o.game_bean.award()
            # o.game_bean.accept()
            # o.award.set_after_award_users_acct_balance(gameId)
            # o.award.print_users_acct_balance_info()
            # o.award.check_users_cash()

def test_temp_lsports():
    """测试用例"""
    case  = ReadRunCaseData('testdata.xlsx')
    o = GamePublicRequest(http='https')
    case_ls = case.get_cases()
    for case_obj in case_ls:
        read_write_info(w_v.event_id_file,'{}')
        case_obj = case_obj[0]
        test_data_obj = case.get_test_data(case_obj.test_dataId)

        testName='(%s)%s'%(case_obj.caseId,case_obj.case_description)
        o.login_and_register.login()
        for i in range(6):
            o.login_and_register.login()
            # o.create_game_info.auto_create_funny()
            eventId = o.create_game_info.create_third_game_lsports(sport=w_v.sport_soccer,noneCenralCurrency_ls=[]
                ,league='',is_get_not_score_play=False,case_data_obj=test_data_obj)

            gameId = o.db.get_gameId(eventId['text'])
            # gameId = o.get_gameIds(is_third=True,index=0)
            # gameId = 594
            o.game_bean.set_gameId(gameId=gameId)
            o.game_bean.submit_review()
            o.game_bean.pending_deployment_review()
            o.game_bean.deployment_review()
            o.game_bean.publish_review('PENDING_RELEASE')
            # 投注
            # o.users_betting(case.get_betting_params_and_users_dict(test_dataId=case_obj.test_dataId
            #                                 ,db = o.ev_obj.db,gameId=gameId,is_third_data=True,
            #                                 game_score=test_data_obj.score))
            # o.game_bean.close
            # o.game_bean.accept


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

            gameId =938     #available: "152.35133191"  2019-06-11 03:46:47.719
            score = '2:1'    #924  "balanceAmt":"150.35133191"
            o.game_bean.set_gameId(gameId=gameId)

            o.game_bean.close()
            o.game_bean.accept()

            # o.game_bean.set_game_score(score='0:5')
            # o.game_bean.fetch_game_amount(score='0:5')
            #
            # o.game_bean.save_win_option_check(win_index=0)  #电竞获胜选项

            o.game_bean.save_score_check(score=score)
            o.login_and_register.login('zhouyali')
            # o.game_bean.save_win_option_check(win_index=0)
            o.game_bean.save_score_check(score=score)

            o.game_bean.calc_award(score=score)   #直接开奖

            # o.game_bean.fetch_game_amount(score='2:1')


            # o.award.set_berfore_award_users_acct_balance(gameId)
            # o.award.set_user_award_amount(gameId,o.game_bean.options_info_dict)
            # #s
            # o.award.set_after_award_users_acct_balance(gameId)
            # o.award.print_users_acct_balance_info()
            # o.award.check_users_cash()

def temp():
    o = GamePublicRequest()
    o.login_and_register.login()
    # o.create_game_info._save_or_read_eventId(32,is_read=False)
    # r = o.create_game_info._save_or_read_eventId(32,is_read=True)
    # print(r)
    # r = o.create_game_info._save_or_read_eventId(45,is_read=True)
    # print(r)
    o.create_game_info._create_game_request_template()


def inser_val():

    # db = MysqlUtil(db='sp_test')
    fp = open('E:/1.sql',encoding='utf-8')
    print(fp.read())


import sys
import re
import os

if __name__ == '__main__':
    # test_temp_lsports()     #建比赛
    # test_temp()
    test001()          #开奖
    # temp()
    # inser_val()
    # print(os.environ)
    # d = {'a':1}
    # print(d.get('b',[]))
    # print(d)

    pass
