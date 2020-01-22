#coding=utf-8
from decimal import Decimal
from coingame.beans.coinGameBeans import OptionInfo
from coingame.beans.dataBean import BettingBean, UserAcctBalanceInfo
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.globalparam import get_project_path
from coingame.module.gamePublicLogic import GamePublicRequest
from public.common.util import OperatorExcel, logger
import re
import time


global_dict = {}

def temp001():
    global  global_dict
    global_dict['b']=200

def test001():
    o = GamePublicRequest()
    headers = o.login_and_register.login()
    # o.set_other_objs_headers(headers)
    # o.create_game_info.create_third_game(sport='Soccer',league='94',eventId=853134)
    # o.create_game_info.create_third_game(sport='Soccer',noneCenralCurrency_ls=[])
    # print(o.get_gameIds(eventId=853134))
    # print(o.get_gameIds())
    # game_ids = o.get_gameIds(is_third=False,game_status='PENDING_RELEASE')
    game_ids = [214]
    for game_id in game_ids:
        print('gameid=',game_id)
        o.game_bean.set_gameId(game_id)
        # o.game_bean.discard('RELEASE_EXCEPTION')
        o.game_bean.submit_review()
        o.game_bean.pending_deployment_review()
        o.game_bean.deployment_review()
        o.game_bean.publish_review('PENDING_RELEASE')
        # o.game_bean.revoke()
        # o.game_bean.accept()
    # o.game_bean.set_gameId(181)
    # o.game_bean.revoke()
    # o.game_bean.close()
    # o.game_bean.get_accept_params()
    # o.game_bean.accept()

def test002():
    case_file = get_project_path()+'/coingame/data/testCaseData/testdata.xlsx'
    excel = OperatorExcel(case_file)
    sql = 'test_data&id<>-1&1'
    o = BettingBean(excel.getData2DictList(sql)[0])
    print(o.get_currency_option_query_condition())

    o1 = GamePublicRequest()
    print('查询结果\n',o1.ev_obj.db.get_game_currency_optionId(o,'ETC'))

def test003():
    o = GamePublicRequest()
    r = o.db.get_betting_info_by_currency_optionId(2745)
    print(r)






def test_award_process():
    o = GamePublicRequest()
    o.login_and_register.login()
    #创建栏目
    # eventId = o.create_game_info.create_third_game(sport='Soccer',noneCenralCurrency_ls=[])
    # gameId = o.get_gameIds(eventId)
    gameId = 220
    o.game_bean.set_gameId(gameId=gameId)
    # o.game_bean.submit_review()
    # o.game_bean.pending_deployment_review()
    # o.game_bean.deployment_review()
    # time.sleep(1)



    # o.game_bean.publish_review('PENDING_RELEASE')

    #投注
    # case  = ReadRunCaseData()
    # betting_params_ls = case.get_betting_params_ls(betting_id='B1'
    #                                     ,db = o.ev_obj.db,gameId=gameId,is_third_data=False)
    # o.login_and_register.login('FH02@qq.com','12345678')
    # for params in betting_params_ls:
    #     o.website.betting(params)

    #封盘 审核通过
    o.game_bean.close()
    # print('下一步')
    # o.game_bean.accept()

    # #开奖
    # o.game_bean.set_game_score('0:1')
    # o.award.set_berfore_award_users_acct_balance(gameId)
    # o.award.set_user_award_amount(gameId,o.game_bean.options_info_dict)
    # o.game_bean.award()
    # o.game_bean.accept()
    # o.award.set_after_award_users_acct_balance(gameId)
    # o.award.print_users_acct_balance_info()
    # o.award.check_users_cash()




def test_re():
    s = "((Decimal('1.000000000000000000'), 'ETC', 2745),)"
    a = ".*1.*, 'ETC', 2745.*"
    print(re.search(a,s))



if __name__ == '__main__':
    # test001()
    # test002()
    # test003()
    # test_award_process()
    test_re()

    pass


