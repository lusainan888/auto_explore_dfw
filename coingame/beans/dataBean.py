#coding=utf-8

import re
from coingame.beans.coinGameBeans import BettingInfo
from public.common.util import  calculate_float_data
from coingame.beans import sql_manager as w_sql



class Categories():

    def __init__(self):
        self.id=0
        self.league=0
        self.level_1_name=''
        self.level_2_name=''
        self.level_3_name=''
        self.level_4_name=''
        self.categoryId=0
        self.source=''
        self.sport=''

    def get_levels_name(self):
        str = '%s->%s->%s'%(self.level_1_name,self.level_2_name,self.level_3_name)
        if self.level_4_name != '':
            return '%s->%s'%(str,self.level_4_name)
        return str

class BettingBean():

    def __init__(self,betting_dict):
        self.__dict__ = betting_dict

    def get_currency_option_query_condition(self,is_third_data=True):
        """获取查询币种的option的查询条件"""
        if is_third_data:
            part_where_condition = "(additional_tag in ('%s','%s','%s') and tag in('%s','%s','%s'))"\
                                   %(self.__my_slip(self.correct_score)[1]
            ,self.__my_slip(self.alternative_asian_handicap)[1]
            ,self.__my_slip(self.alternative_goal_line)[1]
            ,self.__my_slip(self.correct_score)[0]
            ,self.__my_slip(self.alternative_asian_handicap)[0]
            ,self.__my_slip(self.alternative_goal_line)[0])

            part_where_condition = re.sub(",''|''",'',part_where_condition).replace('(,','(')
            if 'additional_tag in ()' in part_where_condition:
                part_where_condition=''

            part_where_condition_1 = "(additional_tag is null and tag in ('%s','%s','%s'))"\
                                     %(self.__my_slip(self.market_1_1)[0]
            ,self.__my_slip(self.double_chance)[0]
            ,self.__my_slip(self.both_teams_to_score)[0])

            part_where_condition_1 = re.sub(",''|''",'',part_where_condition_1).replace('(,','(')
            if 'tag in ()' in part_where_condition_1:
                part_where_condition_1=''

            part_where_condition = '('+part_where_condition+ ' or ' + part_where_condition_1+')'
            part_where_condition = re.sub("^\( or",'(',part_where_condition)
            part_where_condition = re.sub("or \)$",')',part_where_condition)
            # print(part_where_condition)

            return ' and '+part_where_condition
        else:
            return ''


    def __my_slip(self,filed,slip_str='&'):
        arr = ['','']
        if filed != '':
            temp_arr = filed.split(slip_str)
            # print(temp_arr,len(temp_arr))
            for i in range(len(temp_arr)):
                arr[i] = temp_arr[i].replace(' ','')
        return arr


class UserAcctBalanceInfo():

    def __init__(self):
        self.old_acct_balance_dict = {}  #开奖前的资产信息 key=currency value=AcctBalance()
        self.after_award_acct_balance_dict = {} #开奖后的资产信息 key=currency value=AcctBalance()
        self.betting_dict = {} #投注信息 key=currency value=BettingInfo
        self.currency_ls = [] #用户的币种

    def set_acct_balance(self,acct_balance_dict_obj,is_old_acct=True):
        """设置用户账户信息"""

        if is_old_acct:
            self.old_acct_balance_dict = acct_balance_dict_obj
            self._set_user_currencys()
        else:
            self.after_award_acct_balance_dict = acct_balance_dict_obj


    def _set_user_currencys(self):
        """"""
        for k in self.old_acct_balance_dict:
            self.currency_ls.append(k)


    def set_users_award_amout(self,option_result_dict):
        """设置用户的中奖金额"""
        for currency,bettingInfo_obj in self.betting_dict.items():
            # bettingInfo_obj = BettingInfo()
            # print(currency,bettingInfo_obj.amount)
            if bettingInfo_obj.amount != 0:
                bettingInfo_obj.set_award_amount(option_result_dict)

        # print('over')


    def set_betting_info(self,betting_info_obj_ls,option_result_dict):
        """设置用户投注信息
        betting_info_obj:BettingInfo
        """
        for betting_info_obj in betting_info_obj_ls:
            # betting_info_obj = BettingInfo()
            # print('投注选项',betting_info_obj.currency,betting_info_obj.optionId)
            betting_info_obj.set_award_amount(option_result_dict)

        for currency in self.currency_ls:
            self.betting_dict.setdefault(currency,BettingInfo())

        #按币种累加投注金额  累加返回金额
        for betting_info_obj in betting_info_obj_ls:
            # betting_info_obj = BettingInfo()
            user_betting_obj = self.betting_dict[betting_info_obj.currency]

            user_betting_obj.amount = calculate_float_data(user_betting_obj.amount,
                                                betting_info_obj.amount,'+')
            user_betting_obj.return_amount = calculate_float_data(user_betting_obj.return_amount,
                                        betting_info_obj.return_amount,'+')


        # print('中奖金额000',self.betting_dict['USDT'].return_amount)

        # for k,v in self.betting_dict.items():
        #     print('投注信息',k,v.amount,v.return_amount)

    def check_frozen_cash(self):
        """检查冻结金额
        开奖后冻结金额=old - 投注金额
        """
        result_str = ''
        up_int = 1000
        for currency,acct_balance in self.old_acct_balance_dict.items():
            new_acct_balance = self.after_award_acct_balance_dict[currency].frozen_cash
            betting_amount = self.betting_dict[currency].amount
            old_acct_balance = acct_balance.frozen_cash
            #需要用round来处理float计算问题 例0.6-0.5返回值为0.0999.. 使用round可解决此问题
            act_balance = round(old_acct_balance - betting_amount,8)
            if new_acct_balance != act_balance:
                result_str += '冻结金额 %s(期望值:%s 实际值:%s) new=%s old=%s ' \
                             'betting=%s\n'%(currency,act_balance,new_acct_balance,
                                              new_acct_balance,old_acct_balance,betting_amount)

        return  result_str

    def check_free_cash(self):
        """检查可用资产
        可用资产=old+开奖后的返回金额
        """
        result_str = ''
        for currency,acct_balance in self.old_acct_balance_dict.items():
            new_acct_balance = self.after_award_acct_balance_dict[currency].free_cash
            award_amount = self.betting_dict[currency].return_amount
            old_acct_balance = acct_balance.free_cash
            act_balance = round(old_acct_balance + award_amount,8)
            if new_acct_balance != act_balance:
                result_str += '可用资产 %s(期望值:%s 实际值:%s) new=%s old=%s ' \
                             'award_amount=%s\n'%(currency,act_balance,new_acct_balance
                                              ,old_acct_balance,old_acct_balance,award_amount)

        return  result_str





class AcctBalance():

    def __init__(self):
        self.currency = ''
        self.frozen_cash = 0.0
        self.free_cash = 0.0

    # def print_info(self):
    #     return


class EventInfo():

    vs = ''
    id = 0
    home_id = 0
    away_id = 0
    start_time = 0

    def __str__(self):
        return self.vs

    def info(self):
        return str(self.id)+' '+ self.vs



if __name__ == '__main__':
    s = """( or a"""
    print(re.sub("^\( or|or $",'',s))



