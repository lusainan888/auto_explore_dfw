#coding=utf-8

"""动态赔率工具"""

from math import ceil, floor
import copy
import requests
import re
import json
from decimal import Decimal
from coingame.beans.public_method import get_public_response
from public.common.log import Log
from coingame.beans import public_values as w_p_v
from coingame.beans import sql_manager as w_sql
from public.common.util import calculate_float_data, sub_str, search_str
from decimal import Decimal
from coingame.module.decorators import check_step_is_success

logger = Log()


class Odds():

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

        self.option_pay_bet_sql="""select c_o_i.option_id,IFNULL(sum(c_o_i.%s),0) pay,IFNULL(sum(c_o_i.%s),0) bet from fortune_base_play_info b_p_i,
                fortune_base_play_option_info b_p_o_i,
                fortune_currency_option_info c_o_i
                where b_p_i.play_id=b_p_o_i.play_id and b_p_o_i.option_id=c_o_i.option_id
                    and b_p_i.game_id=%s %s GROUP BY c_o_i.option_id;
                """
        self.mysqlinfo=self.ev_obj.db.mysqlinfo


    @check_step_is_success('检查最终赔率')
    def check_game_finally_odds(self,gameId,plays_ls=[]):
        """检查最终赔率
        plays_ls=[] value=[playId,market] 例： plays_ls=[2365,'correct_score']
        """
        check_result = ''
        if len(plays_ls) == 0:
            plays_ls = self.ev_obj.db.get_game_plays(gameId)
        for play in plays_ls:
            playId = play[0]
            market = play[1]
            print('开始测试：',market)
            if market == w_p_v.alternative_asian_handicap:
                #获取让分盘的盘口
                sql = w_sql.additional_tag%(playId,'homeOd')
                additional_tag_ls = self.mysqlinfo.selectInfo(sql)
                for additional_tag in additional_tag_ls:
                    handicap = additional_tag[0]
                    check_result += self.get_finally_odds(gameId,playId,handicap)
                pass

            elif market == w_p_v.alternative_goal_line:
                #获取大小盘的盘口
                sql = w_sql.additional_tag%(playId,'overOd')
                additional_tag_ls = self.mysqlinfo.selectInfo(sql)
                for additional_tag in additional_tag_ls:
                    handicap = additional_tag[0]
                    check_result += self.get_finally_odds(gameId,playId,handicap,True)
                pass
            elif market == w_p_v.correct_score or market == w_p_v.double_chance:
                #正确比分 和 双胜彩
                check_result += self.get_finally_odds(gameId,playId,all_is_master=True)
            else:
                check_result += self.get_finally_odds(gameId,playId)

        return get_public_response(check_result)


    def get_pay_currency(self):
        #获取有效的货币
        sql=w_sql.dynamic_currency
        r = self.mysqlinfo.selectInfo(sql)
        pay = 'total_pay_eur'
        bet = 'total_bet_eur'
        if r[0][0]=='USD':
            pay = 'total_pay_usd'
            bet = 'total_bet_usd'
        return [pay,bet]

    def get_finally_odds(self,gameId,playId=None,handicap='',
                         is_goal_line=False,all_is_master=False):
        """获取最终赔率"""
        playId001 = playId
        old_handicap = handicap
        pay_bet = self.get_pay_currency()
        pay = pay_bet[0]
        bet = pay_bet[1]

        if playId==None:
            playId=''
        else:
            playId='and b_p_i.play_id=%s'%playId
            if handicap != '':
                home_tag='homeOd'
                away_tag = 'awayOd'
                homeHandicap = handicap
                awayHandicap = self.get_away_handicap(homeHandicap)
                if is_goal_line:
                    #如果是大小球
                    home_tag='overOd'
                    away_tag = 'underOd'

                playId ="""and (additional_tag='%s' and tag='%s'
                    or( additional_tag='%s' and tag='%s'))"""\
                          %(homeHandicap,home_tag,awayHandicap,away_tag)

        sql=self.option_pay_bet_sql%(pay,bet,gameId,playId)
        #获取一个玩法下所有的选项 optionid pay(赔付总和) bet(投注总和)
        # print(sql)
        result = self.mysqlinfo.selectInfo(sql)
        result=list(result)
        total_bet = self.get_total_bet(result,2)
        #按赔付值降序排列
        result=self.list_order_by_desc(result)
        result=self.db_Decimal_to_float(result)
        # print('总投注值：',total_bet,'最大赔付值：',result[0][1])
        k = self.getK(len(result),result[0][1]-total_bet)
        print('计算的K值：',k)
        exp_result_dict = self.get_option_final_odds(result,k,total_bet,all_is_master)
        #检查数据库的最终赔率
        return_str = self.check_db_final_odds(exp_result_dict)
        return_str += self.check_fortune_modify_odds_record(playId001,handicap)
        if return_str != '':
            print('gameId:%s playId:%s handicap:%s \n%s'%(
                gameId,playId001,old_handicap,return_str))

        return return_str



    def get_option_final_odds(self,option_ls,k,total_bet,all_is_master=False):
        """获取选项的最终赔率"""
        return_res_ls={}
        option_odds_result = self.get_all_option_odds(option_ls)
        # for i in range(len(option_ls)):
        #     print('通过抽水计算的当前赔率',option_ls[i][0],option_odds_result[i])

        master_final_odds = self.get_master_final_odds(option_odds_result[0],k)
        return_res_ls[option_ls[0][0]]=master_final_odds
        if all_is_master:
            for i in range(0,len(option_odds_result)):
                return_res_ls[option_ls[i][0]]=option_odds_result[i]
            return return_res_ls

        # print(option_ls[0][0],'主动项的最终赔率',master_final_odds)
        option_count=len(option_ls)
        if option_count==2:
            return_res_ls[option_ls[1][0]]=self.get_two_other_final_odds(master_final_odds,option_odds_result,k)
        elif option_count==3:
            method = 0 #0代表一正一负 1代表2负
            if option_ls[1][1]-total_bet<0:
                method=1
            result = self.get_three_other_final_odds(master_final_odds,option_odds_result,k,method)
            for i in range(1,3):
                return_res_ls[option_ls[i][0]]=result[i]
        else:
            #大于3选项
            pass

        # for k in return_res_ls:
        #     print('最终赔率',k,return_res_ls[k])
        return return_res_ls

    def get_three_other_final_odds(self,master_final_odds_result,option_odds_result,k,method):
        """获取3项被动项的最终赔率"""
        a = option_odds_result[0]
        b = option_odds_result[1]
        c = option_odds_result[2]

        for i in range(len(master_final_odds_result)):
            if master_final_odds_result[i][0] != None:
                a_currency_new = master_final_odds_result[i][1]
                a_currency_old = a[i][1]
                b_currency_old = b[i][1]
                c_currency_old = c[i][1]
                temp_v=None
                if method==1:
                    #2负
                    if k<1.4:
                        temp_v=1/((1/a_currency_old-1/a_currency_new)/(1/b_currency_old+1/c_currency_old)+1)
                    else:
                        temp_v=1/((1/a_currency_old-1/((a_currency_old-1)/1.3+1))/(1/b_currency_old+1/c_currency_old)+1)
                    b[i][1] = self.truncate(b_currency_old*temp_v,2)
                    c[i][1] = self.truncate(c_currency_old*temp_v,2)
                else:
                    #一正一负
                    if k<1.4:
                        temp_v=1/((a_currency_old+c_currency_old)/(a_currency_old*c_currency_old)-1/a_currency_new)
                    else:
                        temp_v=1/((a_currency_old+c_currency_old)/(a_currency_old*c_currency_old)-1/((a_currency_old-1)/1.3+1))
                    c[i][1]=self.truncate(temp_v,2)
                a[i][1]=a_currency_new
                if k == 1:
                    b[i][1] = b_currency_old
                    c[i][1] = c_currency_old

        return option_odds_result


    def get_master_final_odds(self,coin_odds_results,k):
        """获取主动项的最终赔率=(通过抽水计算的原赔率-1)/k+1"""

        final_odds = copy.deepcopy(coin_odds_results)
        for odds in final_odds:
            odds[1]=self.truncate((odds[1]-1)/k+1,2)
            # odds.pop()
        return final_odds


    def get_two_other_final_odds(self,master_final_odds_result,option_odds_result,k):
        """获取2项被动项的最终赔率"""
        for i in range(len(master_final_odds_result)):
            a = master_final_odds_result[i][1]
            a_old=option_odds_result[0][i][1]
            b_old = option_odds_result[1][i][1]
            if k == 1:
                b_new = b_old
            elif 1<k<1.4:
                b_new = self.truncate(1/((a_old+b_old)/(a_old*b_old)-1/a),2)
            else:
                b_new = self.truncate(1/((a_old+b_old)/(a_old*b_old)-1/((a_old-1)/1.3+1)),2)
            option_odds_result[1][i][1]=b_new
        # print('结果：',option_odds_result[1])
        return option_odds_result[1]


    def get_all_option_odds(self,options_ls):
        """获取所有选项的 原赔率=(赔率-1)*(1-抽水)+1"""
        res_ls=[]
        for o in options_ls:
            res_ls.append(self.get_odds(o[0]))

        return res_ls


    def get_odds(self,option_id,is_print=False):
        """获取原赔率=(赔率-1)*(1-抽水)+1"""
        sql = "select original_odds from fortune_base_play_option_info where option_id='%s';"%option_id
        r=self.mysqlinfo.selectInfo(sql)
        original_odds=float(r[0][0])
        sql = "select currency,shrink,central from fortune_currency_option_info where option_id='%s';"%option_id
        result = self.mysqlinfo.selectInfo(sql)
        odds_result=[]
        for r in result:
            shrink = float(r[1])
            t=(original_odds-1)*(1-shrink)
            odds = self.truncate((t*100+1*100)/100,2) #这做的目的是因为 1+0.36=1.359999 (原因不知)
            odds_result.append([r[0],odds,str(r[2]).replace("b'\\x0","").replace('\'','')])

        if is_print:
            print(option_id,'通过抽水计算的赔率',odds_result)
        return odds_result

    def db_Decimal_to_float(self,db_result):
        """把数据库的Decimal转换成float"""
        res_ls = []
        for db in db_result:
            db = list(db)
            for i in range(len(db)):
                if isinstance(db[i],Decimal):
                   db[i] = float(db[i])
            res_ls.append(db)
        # print(res_ls)
        return res_ls

    def get_total_bet(self,result_ls,index):
        """获取总投注"""
        total_bet = 0
        for r in result_ls:
            total_bet = total_bet+r[index]
        return float(total_bet)

    def list_order_by_desc(self,play_option_ls,index=1):
        """按赔付值的最大值降序排序"""
        count = len(play_option_ls)
        for i in range(count):
            for j in range(i+1,count):
                if play_option_ls[j][index]>play_option_ls[i][index]:
                    play_option_ls[i],play_option_ls[j]=play_option_ls[j],play_option_ls[i]
        # print('降序排列',play_option_ls)
        return play_option_ls

    def getK(self,option_type,max_pay):
        """计算K值"""
        num = 5
        if max_pay<=0:
            return 1
        if option_type>2:
            option_type='01'
            num=6
        else:
            option_type='00'
        sql = "SELECT pay_amount,set_factor from fortune_option_odds_gradient where is_effect='00' and option_type='%s'; "%(option_type)
        r = self.mysqlinfo.selectInfo(sql)
        for i in range(num-1):
            # print(i)
            gradient001= float(r[i][0])
            gradient002= float(r[i+1][0])

            if i==0:
                if max_pay<=r[i][0]:
                    return self.truncate(0.1/gradient001*max_pay+1,2)
            if num-2<=i<=num-1:
                if num==5:
                    return 1.4
                else:
                    return 1.5
            if r[i][0]<max_pay<=r[i+1][0]:
                # print(r[i+1][1])
                return self.truncate(0.1/(gradient002-gradient001)*(max_pay-gradient001)+float(r[i+1][1]),2)

    def truncate(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        v =  '.'.join([i, (d+'0'*n)[:n]])
        return float(v)

    def get_db_final_odds(self,optionId):
        """获取数据库的最终赔率"""
        sql = 'select currency,final_odds,central from fortune_currency_option_info where option_id=%s;'%optionId
        result = list(self.mysqlinfo.selectInfo(sql))
        res = []
        result = self.db_Decimal_to_float(result)
        for r in result:
            r = list(r)
            r[2] = str(r[2]).replace("b'\\x0","").replace('\'','')
            res.append(r)
        return res

    def check_db_final_odds(self,expected_result_dict):
        """检查数据库的最终赔率是否正确"""
        result = ''
        for exp_optionId in expected_result_dict:
            act = self.get_db_final_odds(exp_optionId)
            exp = expected_result_dict[exp_optionId]
            # print('期望值：',exp)
            # print('实际值：',act)
            if str(act) != str(exp):
                result += '选项%s 的最终赔率计算不正确\n期望值：%s\n实际值：%s\n'\
                         %(exp_optionId,exp,act)
                # print('选项%s 的最终赔率计算不正确'%exp_optionId)
                # print('期望值：',exp)
                # print('实际值：',exp)
            else:
                # print('选项%s 计算结果与数据库一致'%exp_optionId)
                pass
        return result

    def check_fortune_modify_odds_record(self,playId,home_handicap=''):
        """检查fortune_modify_odds_record的赔率记录是否正确"""

        return_str = ''
        additional_tag = ''
        if home_handicap != '':
                additional_tag = " and ((additional_tag in ('%s') and tag in ('homeOd','overOd'))" \
                                 " or (additional_tag in ('%s') and tag in ('awayOd','underOd')));"\
                                %(home_handicap,self.get_away_handicap(home_handicap))

        sql = w_sql.option_ids%(playId)+additional_tag
        result = self.mysqlinfo.selectInfo(sql)
        options = re.sub('\(|,\)|\)','',str(result))
        print('选项optionId',options)
        sql = 'SELECT id,currency from fortune_currency_play_info WHERE play_id=%s and central=0;'%playId
        result = self.mysqlinfo.selectInfo(sql)
        for r in result:
            currency=r[1]
            currency_play_id=r[0]
            sql = """
                select final_odds,address,id from fortune_currency_option_info
                  where option_id in (%s) and currency='%s' AND central=0;
                """%(options,currency)
            exp_ls = self.db_Decimal_to_float(self.mysqlinfo.selectInfo(sql))
            handicap = ''
            if home_handicap != '':
                handicap = "and handicap in ('%s','%s')"\
                                %(home_handicap,self.get_away_handicap(home_handicap))

            sql = w_sql.modify_odds%(currency_play_id,handicap)
            act_ls = self.mysqlinfo.selectInfo(sql)
            act_str= str(act_ls)
            # act_str =re.sub('"optionId":|"optionAddress":|"odds":','',act_str)

            for exp in exp_ls:
                exp_odds = exp[0]
                exp_addr = exp[1]
                reg = '.*({.*?%s})'%exp[2]
                act_temp = search_str(reg,act_str,1)
                if act_temp == '':
                    reg = '.*({.*?%s,.*?})'%exp[2]
                    act_temp = search_str(reg,act_str,1)
                if act_temp != '':
                    act_dict = json.loads(act_temp,encoding='utf-8')
                    if exp_odds != float(act_dict['odds']) or exp_addr != act_dict['optionAddress']:
                        return_str += '期望值：%s\n实际值：%s'%(str(exp),act_temp)
                else:
                    return_str += '数据库中没有：%s\n'%exp

            if return_str != '':
                return_str = 'fortune_modify_odds_record表保存最终赔率不正确：\n'+return_str

        return return_str


    def get_away_handicap(self,homeHandicap):
        """获取客队的盘口"""
        #算出客队盘口
        awayHandicap = ''
        if '+' in homeHandicap:
            awayHandicap = re.sub('\+','-',homeHandicap)
        elif '-' in homeHandicap:
            awayHandicap = re.sub('-','+',homeHandicap)
        else:
            awayHandicap = homeHandicap
        return awayHandicap

if __name__=='__main__':
    odds = Odds(dbName='sp_test')
    odds.get_finally_odds(251,566)
    # odds.check_fortune_modify_odds_record(540)
    # odds.get_db_final_odds(1913)
