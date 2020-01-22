#coding=utf-8

import re
from coingame.beans.dataBean import BettingBean
from public.common.util import OperatorExcel, dict_to_obj
from coingame.config.globalparam import get_project_path
import json
from coingame.beans import public_values as w_p_v

class ReadRunCaseData():
    """读取测试用例信息"""

    def __init__(self,case_file='',other_path=None):
        if other_path == None:
            self.case_file = get_project_path()+'/coingame/data/testCaseData/'+case_file
        else:
            self.case_file = other_path
        self.excel = OperatorExcel(self.case_file)

    def get_betting_users(self,b_u_id):
        """获取用例投注信息"""
        result_dict = {} #key=user_name
        sql = 'betting_users&b_u_id=%s,isRun=yes&0'%b_u_id
        users_ls = self.excel.getData2DictList(sql)
        return users_ls


    def get_betting_params_and_users_dict(self,test_dataId,db=None,
                                gameId=None,is_third_data=True,
                                sport_type=w_p_v.sport_soccer,game_score=''):
        """获取投注请求数据
        db = coinGameDb
        """
        if game_score != '':
            sport_type = ''
        # db = coinGameDb()
        result_dict = {}
        sql = 'test_data&betting_id=%s&0'%test_dataId
        res_ls = self.excel.getData2DictList(sql)
        params_ls_str = []
        users_ls = []
        for res in res_ls:
            #获取投注用户
            sql = 'betting_users&b_u_id=%s,isRun=yes&0'%res['b_u_id']
            users = self.excel.getData2DictList(sql)
            for u in users:
                users_ls.append(u)

            #获取投注请求参数
            b = BettingBean(res)
            sql = 'betting_currency&betting_id=%s,isBeting=yes&0'%b.betting_currency_id
            currency_ls = self.excel.getData2DictList(sql)
            for currency_dict in currency_ls:
                optionId_ls = []
                if b.sport_type == w_p_v.sport_soccer\
                        or sport_type == w_p_v.sport_basktball:
                    #如果是足球 篮球
                    optionId_ls = db.get_game_currency_optionId(b,currency_dict['currency'],
                                                            gameId=gameId,is_third_data=is_third_data)
                else:
                    #如果是其它类型 则取第一个玩法的 第一个optionId
                    play_ls = db.get_game_plays(gameId)
                    optionId_ls = db.get_game_currency_optionId(b,currency_dict['currency'],
                                                gameId=gameId,sport_type='',playId=play_ls[0][0])
                    optionId_ls = [optionId_ls[0]]

                currency_params = {}
                currency_params['records']=[]
                currency_params['currency']=currency_dict['currency']
                currency_params['language']=currency_dict['language']
                for optionId in optionId_ls:
                    temp_dict = {}
                    temp_dict['currencyOptionId']=optionId[0]
                    temp_dict['amount']=currency_dict['amount']
                    temp_dict['odds']=float(optionId[1])
                    currency_params['records'].append(temp_dict)
                params_ls_str.append(json.dumps(currency_params))

        # for p in params_ls_str:
        #    print('投注请求参数\n',p)
        result_dict.setdefault('users',users_ls)
        result_dict.setdefault('betting_params',params_ls_str)
        return result_dict


    def get_test_data(self,test_dataId):
        """获取用例测试数据
        """
        result_dict = {}
        sql = 'test_data&betting_id=%s&1'%test_dataId
        res_ls = self.excel.getData2DictList(sql)
        return dict_to_obj(res_ls[0])

    def get_cases(self):
        """获取测试用例"""
        result_ls = []
        sql = 'cases&isRun=yes&0'
        cases_ls = self.excel.getData2DictList(sql)
        for c in cases_ls:
            temp_ls = []
            temp_ls.append(dict_to_obj(c))
            result_ls.append(temp_ls)
        return result_ls






if __name__ == '__main__':
    s = """( or a"""
    print(re.sub("^\( or|or $",'',s))



