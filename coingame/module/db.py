#coding=utf-8
from coingame.beans.coinGameBeans import BettingInfo
from coingame.beans.dataBean import BettingBean, AcctBalance
from public.common.publicUtil import MysqlUtil
import re
from public.common.util import logger
from coingame.beans import sql_manager as w_sql
from coingame.beans import public_values as w_p_v


class coinGameDb():

    # def __init__(self,host='172.17.1.128',db='sp_test'):
    #     self.mysqlinfo=MysqlUtil(host=host,db=db)
    def __init__(self,db='sp_test'):
        if db =='sp_inte':
            self.mysqlinfo=MysqlUtil(db='sp_inte',host='172.17.3.156',user='dev',pwd='dev123')
            print("1")
        elif db == 'sp_beta':
            self.mysqlinfo=MysqlUtil(db=db,host='172.17.3.163')
            print("2")
        else:
            self.mysqlinfo=MysqlUtil(db=db) #testing
            print("3")
    def get_gameId(self,eventId):
        """根据eventId获取gameId"""
        sql = 'SELECT game_id from fortune_base_game_info where outer_event_id=%s' \
              ' and  deleted=0;'%eventId
        try:
            res = self.mysqlinfo.selectInfo(sql)
            return res[0][0]
        except:
            return None

    def get_game_currency_optionId(self,betting_obj:BettingBean,currency,gameId=None,
                                   is_third_data=True,playId=None,
                                   sport_type=w_p_v.sport_soccer):
        """根据gameId获取 币种的optionId
        betting_obj: BettingBean
        """
        play_query = ''
        handicap_query = ''
        if gameId == None:
            gameId = self.get_gameId(betting_obj.event_id)
        if playId != None:
            play_query = ' and b_p_i.play_id in (%s)'%playId
        if sport_type == w_p_v.sport_soccer:
            handicap_query = betting_obj.get_currency_option_query_condition(True)

        sql = """
            SELECT c_o_i.id ,c_o_i.final_odds from
		fortune_base_play_info b_p_i,fortune_base_play_option_info b_p_o_i,fortune_currency_option_info c_o_i
			where b_p_i.play_id=b_p_o_i.play_id and central=1 %s
						and c_o_i.option_id=b_p_o_i.option_id and b_p_i.game_id=%s and c_o_i.currency='%s' %s;
        """%(handicap_query,gameId,currency,play_query)

        logger.info('查询投注currency_optionId：%s'%sql)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            if is_third_data:
                return res
            else:
                # resutl = []
                # resutl.append(res)
                return res

        except:
            return None

    def get_currency_playId_ls(self,playId,status = ''):
        """获取币种的玩法id"""
        if status != '':
            status = "and `status`='%s'"%status
        sql = "SELECT id,currency from fortune_currency_play_info WHERE play_id=%s  %s ;"%(playId,status)
        # print(sql)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            # print(res)
            return res
        except:
            return None

    def get_currency_optionId_ls(self,optionId,currency,index=0):
        """获取币种的optionId"""
        sql = "SELECT id from fortune_currency_option_info where option_id in (%s) and currency='%s' ;"\
              %(optionId,currency)
        # print(sql)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            # print(res)  #元组转列表
            res_ls = []
            for r in res:
                res_ls.append(r[index])
            print(res_ls)
            return res_ls
        except:
            return None

    def get_gametype(self,gameId):

        sql = 'SELECT game_type from fortune_base_game_info WHERE game_id=%s;'%gameId

        try:
            res = self.mysqlinfo.selectInfo(sql)
            return res[0][0]
        except:
            return None

    def get_currency_play_info(self,gameId,status=None,index=0):
        """获取gameId 的某一个状态的currency_play_info"""
        if status == None:
            sql_status=''
        else:
            sql_status = "and c_p_i.`status`='%s'"%status

        sql='''
            SELECT c_p_i.id from fortune_base_play_info b_p_i,fortune_currency_play_info c_p_i
	          WHERE b_p_i.play_id=c_p_i.play_id and b_p_i.game_id=%s %s;
        '''%(gameId,sql_status)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            res_ls = []
            for r in res:
               res_ls.append(r[index])
            return res_ls
        except:
            return None

    def get_betting_info_obj_ls(self,currency_play_ids,user_id='',is_get_users=False,index=0):
        """获取投注信息 返回[BettingInfo]"""
        group_by = ''
        if user_id !='':
            user_id = ' and b.user_id=%s'%user_id
        if type(currency_play_ids) == list:
            currency_play_ids = re.sub('\[|]','',str(currency_play_ids))
        find_fields = 'b.currency_option_id,b.odds,b.amount,b.currency,c_o_i.option_id'
        if is_get_users:
            find_fields = 'b.user_id'
            group_by = 'GROUP BY b.user_id'
        sql='''
            SELECT  %s from fortune_betting_record b,fortune_currency_option_info c_o_i
              where  c_o_i.id=b.currency_option_id and currency_play_id in (%s) %s %s;
        '''%(find_fields,currency_play_ids,user_id,group_by)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            res_ls = []
            if is_get_users:
                for r in res:
                   res_ls.append(r[index])
                return res_ls
            else:
                # logger.info('用户投注查询sql：\n'+sql+'\n')
                for r in res:
                    betting_obj = BettingInfo()
                    betting_obj.currency_option_id=r[0]
                    betting_obj.odds = float(r[1])
                    betting_obj.amount = float(r[2])
                    betting_obj.currency = r[3]
                    betting_obj.optionId = r[4]
                    res_ls.append(betting_obj)
            return res_ls
        except:
            return None

    def get_user_acct_balance_dict(self,userId):
        """获取用户的acct_balance_obj
        返回dict:key=currency,value=AcctBalance
        """
        result_dict = {}
        sql = 'SELECT currency,frozen_cash,free_cash from acct_balance WHERE user_id=%s;'%userId
        # print(sql)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            # print(res)
            for r in res:
                acct = AcctBalance()
                acct.currency = r[0]
                acct.frozen_cash = float(r[1])
                acct.free_cash = float(r[2])
                result_dict[acct.currency]=acct
            return result_dict
        except:
            return None

    def get_betting_info_by_currency_optionId(self,currency_optionId,userId=''):
        """"""

        if userId != '':
            userId = 'and user_id =%s'%userId

        sql = """SELECT b_r.amount,b_r.currency,b_r.currency_option_id from fortune_betting_record b_r
		      WHERE currency_option_id in(%s) ;"""%(currency_optionId,userId)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            return res
        except:
            return None

    def get_userId(self,email):
        sql = "SELECT id from users where email='%s';"%email
        try:
            res = self.mysqlinfo.selectInfo(sql)
            return res[0][0]
        except:
            return None

    def update_acct_balance(self,emails):

        sql = "UPDATE acct_balance set free_cash=10000 where " \
              "user_id in(SELECT id from users where email in(%s));"%emails
        self.mysqlinfo.update(sql)


    def get_play_currency_play_and_optionId(self,gameId='',playId=''):
        play_query = 'and b_p_i.game_id=%s'%gameId
        if playId != '':
            play_query = 'and p_o_i.play_id = %s and b_p_i.game_id=%s'%(playId,gameId)

        sql = """
            SELECT c_p_i.id,c_o_i.id,c_o_i.currency from fortune_currency_option_info c_o_i,fortune_base_play_info b_p_i,
	fortune_base_play_option_info p_o_i,fortune_currency_play_info c_p_i
		where c_o_i.option_id = p_o_i.option_id
			and c_p_i.play_id=p_o_i.play_id and c_o_i.currency=c_p_i.currency and b_p_i.play_id=p_o_i.play_id
				%s;
        """%play_query

        try:
            res = self.mysqlinfo.selectInfo(sql)
            return res
        except:
            return None

    def get_game_plays(self,gameid):
        sql = w_sql.game_plays%gameid
        return self.public_query_info(sql)

    def public_query_info(self,sql,index = None):
        logger.info('查询语句：%s'%sql)
        try:
            res = self.mysqlinfo.selectInfo(sql)
            if index != None:
                return res[0][0]
            return res
        except:
            return None


if __name__=='__main__':
    a=coinGameDb("sp_test")
    gameId=a.get_gameId("4832793")
    # a=coinGameDb("sp_beta")
    # gameId=a.get_gameId("4544434")  #4832793 testing \ 4544434 beta
    # cur_opid=a.get_game_currency_optionId()
    # cur_ply=a.get_currency_playId_ls("1425",'AWARDED') #fortune_currency_play_info
    # cur_opid2=a.get_currency_optionId_ls('14207,14208','BTC') # fortune_currency_option
    a.get_user_acct_balance_dict(1006)
    pass