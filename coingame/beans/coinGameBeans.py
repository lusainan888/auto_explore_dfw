#coding=utf-8


# AWARD/HALF_WIN/HALF_LOST/DRAW

import re
import requests
import json
from coingame.module.decorators import check_step_is_success
from public.common.util import dict_to_obj, calculate_float_data
from coingame.beans import public_values as p_v
from coingame.beans import public_method as p_m
from coingame.beans import api_request_path_manager as api_m
from coingame.beans import sql_manager as w_sql
import time
from public.common.util import logger



#获奖状态

BONUS_AWARD = 'AWARD' #赢
BONUS_LOST = 'LOST' #输
# BONUS_DRAW = 'DRAW' #平局
BONUS_HALF_WIN = 'HALF_WIN' #赢一半退一半
BONUS_HALF_LOST = 'HALF_LOST' #输一半退一半
BONUS_CANCEL = 'DRAW' #退回

#足球比赛类型
MARKET_1_1='1_1' #胜平负
DOUBLE_CHANCE='double_chance' #双胜彩
CORRECT_SCORE='correct_score' #正确比分
BOTH_TEAMS_TO_SCORE='both_teams_to_score' #两队均得分
ALTERNATIVE_ASIAN_HANDICAP='alternative_asian_handicap' #附加让分盘
ALTERNATIVE_GOAL_LINE='alternative_goal_line' #附加大小球

#篮球 网球 棒球 飞比赛类型
MARKET_data_1='\d+_1' #胜负
MARKET_data_2='\d+_2' #让分
MARKET_data_3='\d+_3' #总分


class GameBean():
    """玩法信息"""

    def __init__(self,ev_obj):
        self.is_go_on_onerror = True #当出错时是否进行下一步操作
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

        self.play_info_ls = []

        # self.modify_shrink_path=self.testUrl+'/games/plays/modify-shrink'
        self.is_all_score_plays = True #全部是比分玩法



    def set_gameId(self,gameId):
        self.gameId = gameId
        self._get_game_text()
        self._get_option_info()
        self.play_info_ls = self.get_play_info_ls()

    def get_play_info_ls(self):
        """获取玩法信息
        返回 PlayBean 链表
        """
        result = []
        for play in self.game_text_obj.playInfoDTOS:
            temp = PlayBean()
            temp.gameId = self.gameId
            temp.playId = play.playId
            # temp.play_name = play.market
            try:
                temp.play_name = play.playName.zh
            except:
                temp.play_name = play.playName
            temp.play_option_num = len(play.optionInfoList)
            temp.handicap = play.handicap

            result.append(temp)
        return result



    def _get_option_info(self):
        """获取选项信息"""
        self.options_info_dict = {}
        for play in self.game_text_obj.playInfoDTOS:
            playId = play.playId
            for o in play.optionInfoList:
                option = OptionInfo()
                option.playId = playId
                option.tag = o.tag
                option.handicap = o.additionalTag
                if option.handicap == None:
                    option.handicap = play.handicap
                    option.is_mul_handicap = False
                option.optionId = o.optionId
                option.play_type = play.market
                option.is_not_score_play_attr = option.is_not_score_play()
                if option.is_not_score_play_attr:
                    self.is_all_score_plays = False
                self.options_info_dict[o.optionId]=option

    def _get_award_request_params(self):
        """
        获取开奖请求参数
        注:只要有退钱给用户都算中奖
        """
        re_dict = {}
        for k,v in self.options_info_dict.items():
            # v = OptionInfo()
            if BONUS_LOST != v.award_status:
                try:
                    ls = re_dict[v.playId]
                    ls.append(v.optionId)
                    re_dict[v.playId]=ls
                except:
                    re_dict.setdefault(v.playId,[v.optionId])
        params_ls = []
        for k,v in re_dict.items():
            res_ls = self.db.get_currency_playId_ls(k)
            # print(k,res_ls)
            for res in res_ls:
                temp_dict = {'currencyPlayId':res[0],'gameId':self.gameId}
                winCurrencyOptionId = self.db.get_currency_optionId_ls(re.sub('\[|]','',str(v)),res[1])
                temp_dict.setdefault('winCurrencyOptionId',winCurrencyOptionId)
                params_ls.append(temp_dict)
        return json.dumps(params_ls,indent=4)




    def set_option_award_result(self,score='',win_option_id_dict=None):
        """
        设置选项中奖情况
        1.score 是比赛比分 例：2:0
        """

        # self.options_info_dict = {}
        for optionId,o in self.options_info_dict.items():
            # option = OptionInfo()
            option = o
            if option.optionId == 19094:
                print(12)
            if win_option_id_dict != None:
                #如果是非比分玩法
                if o.is_not_score_play():
                    win_option_id = win_option_id_dict.get(option.optionId)
                    if win_option_id != None:
                        option.award_status = BONUS_AWARD
                    else:
                        option.award_status = BONUS_LOST

            elif option.play_type == ALTERNATIVE_ASIAN_HANDICAP\
                     or re.search(MARKET_data_2,option.play_type):
                #比赛类型为 附加让分盘
                mul_handicap = True
                if re.search(MARKET_data_2,option.play_type):
                    mul_handicap = False
                option.award_status = self._set_alternative_asian_handicap_option_award_result(score,
                                          option.handicap,option.is_home(),mul_handicap=mul_handicap)

            elif option.play_type == ALTERNATIVE_GOAL_LINE\
                     or re.search(MARKET_data_3,option.play_type):
                #比赛类型为 附加大小球
                option.award_status = self._set_alternative_goal_line_option_award_result(score,
                                                                         option.handicap,option.is_under())

            elif option.play_type == MARKET_1_1:
                #比赛类型为 胜平负 胜负
                option.award_status = self._set_market_1_1_option_award_result(score,option.tag)

            elif re.search(MARKET_data_1,option.play_type):
                #胜负
                option.award_status = self._set_win_lose_option_award_result(score,option.tag)

            elif option.play_type == DOUBLE_CHANCE:
                #比赛类型为 双胜彩
                option.award_status = self._set_double_chance_option_award_result(score,option.tag)

            elif option.play_type == CORRECT_SCORE:
                #比赛类型为 正确比分
                option.award_status = self._set_correct_score_option_award_result(score,
                                                            option.handicap,option.tag)

            elif option.play_type == BOTH_TEAMS_TO_SCORE:
                #比赛类型为 两队均得分
                option.award_status = self._set_both_teams_to_score_option_award_result(score,option.tag)
            else:
                #如果是非比分玩法
                if o.is_not_score_play() == False:
                    option.award_status = self._set_two_option_award_result(score,option.tag)
            # option.print_option_award_result()

    def _set_both_teams_to_score_option_award_result(self,score,option_tag):
        """设置选项 两队均得分 获奖结果
        score 比分  option_tag(homeOd drawOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        sub_goal = home_goal - away_goal
        if option_tag == 'Y':
            if home_goal > 0  and away_goal > 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        else:
            if home_goal == 0  or  away_goal == 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        return result

    def _set_correct_score_option_award_result(self,score,option_additionalTag,option_tag):
        """设置选项 正确比分 获奖结果
        score 比分  option_tag(homeOd drawOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        score = score.replace(':','-')
        if option_tag == 'awayOd':
            score = str(away_goal)+'-'+str(home_goal)
        if option_additionalTag == score:
            result = BONUS_AWARD #赢
        else:
            result = BONUS_LOST #输
        return result

    def _set_double_chance_option_award_result(self,score,option_tag):
        """设置选项 双胜彩获奖结果
        score 比分  option_tag(homeOd drawOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        sub_goal = home_goal - away_goal
        if option_tag == 'homeOd_drawOd':
            if sub_goal >= 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        elif option_tag == 'homeOd_awayOd':
            if sub_goal != 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        elif option_tag == 'awayOd_drawOd':
            if sub_goal <= 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        return result

    def _set_market_1_1_option_award_result(self,score,option_tag):
        """设置选项 胜平负获奖结果
        score 比分  option_tag(homeOd drawOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        sub_goal = home_goal - away_goal
        if option_tag == 'homeOd':
            if sub_goal > 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        elif option_tag == 'drawOd':
            if sub_goal == 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        elif option_tag == 'awayOd':
            if sub_goal < 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        return result

    def _set_win_lose_option_award_result(self,score,option_tag):
        """设置选项 胜负获奖结果
        score 比分  option_tag(homeOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        sub_goal = home_goal - away_goal
        if option_tag == 'homeOd':
            if sub_goal > 0:
                result = BONUS_AWARD #赢
            elif sub_goal == 0:
                result = BONUS_CANCEL #退回
            else:
                result = BONUS_LOST #输

        elif option_tag == 'awayOd':
            if sub_goal < 0:
                result = BONUS_AWARD #赢
            elif sub_goal == 0:
                result = BONUS_CANCEL #退回
            else:
                result = BONUS_LOST #输
        return result

    def _set_two_option_award_result(self,score,option_tag):
        """设置选项 2选项的比分玩法
        score 比分  option_tag(homeOd awayOd)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        sub_goal = home_goal - away_goal
        if sub_goal == 0:
            return BONUS_CANCEL #退回

        if option_tag == 'homeOd':
            if sub_goal > 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        elif option_tag == 'awayOd':
            if sub_goal < 0:
                result = BONUS_AWARD #赢
            else:
                result = BONUS_LOST #输
        return result

    def _set_alternative_asian_handicap_option_award_result(self,score,
                                        handicap,is_home,mul_handicap=True):
        """设置选项附加让分盘获奖结果
        score 比分  handicap 盘口  is_home(是否是主队) mul_handicap(是否是多盘口)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        handicap = re.sub("\+",'',handicap)
        if ', ' in handicap or ',' in handicap:
            handicap = handicap.replace(', ',',')
            handicap = (float(handicap.split(',')[0])+float(handicap.split(',')[1]))/2
        else:
            handicap = float(handicap)
        sub_goal = 0
        if is_home:
            home_goal=home_goal+handicap
            sub_goal = home_goal-away_goal
        else:

            if mul_handicap == False:
                away_goal=away_goal-handicap
            else:
                away_goal=away_goal+handicap
            sub_goal = away_goal - home_goal

        if sub_goal >= 0.5:
            result = BONUS_AWARD #赢
        elif sub_goal == 0.25:
            result = BONUS_HALF_WIN #赢一半 输一半
        elif sub_goal == 0:
            result = BONUS_CANCEL #退回
        elif sub_goal == -0.25:
            result = BONUS_HALF_LOST #输一半 赢一半
        elif sub_goal <= -0.5:
            result = BONUS_LOST #输

        return result

    def _set_alternative_goal_line_option_award_result(self,score,handicap,is_under):
        """设置选项附加大小球获奖结果
        score 比分  handicap 盘口  is_under(是否是低于)
        """
        result = ''
        home_goal = int(score.split(':')[0]) #主队进球
        away_goal = int(score.split(':')[1]) #客队进球
        handicap = re.sub("\+",'',handicap)
        handicap = handicap.replace(', ',',')
        if ',' in handicap:
            handicap = (float(handicap.split(',')[0])+float(handicap.split(',')[1]))/2
        else:
            handicap = float(handicap)
        result_goal = home_goal + away_goal - handicap

        if is_under:
            result_goal = 0- result_goal

        if result_goal >= 0.5:
            result = BONUS_AWARD #赢
        elif result_goal == 0.25:
            result = BONUS_HALF_WIN #赢一半 输一半
        elif result_goal == 0:
            result = BONUS_CANCEL #退回
        elif result_goal == -0.25:
            result = BONUS_HALF_LOST #输一半 赢一半
        elif result_goal <= -0.5:
            result = BONUS_LOST #输

        return result



    def _get_game_text(self):
        # url = self.get_game_info_path%self.gameId
        # game_info = self.session.get(url,headers=self.headers).text
        url = api_m.get_game_info%self.gameId
        game_info = self.ev_obj.public_send_request(url).text
        game_info_dict = json.loads(game_info,encoding='utf8')
        self.game_text = game_info_dict
        self.game_text_obj = dict_to_obj(self.game_text)




    def get_close_params(self):
        """获取封盘请求参数"""
        self._get_game_text()
        play_status = 'IN_PREDICTION'
        params_ls = []
        reason = 'auto_test'
        for play in self.game_text_obj.playInfoDTOS:
            for k,v in play.centralCurrencyPlayInfoDTOEnumMap.__dict__.items():
                if '__' not in k:
                    if v.status == play_status:
                        temp_dict = {"gameId":str(self.gameId),
                                      "reason":reason,"currencyPlayId":v.id}
                        params_ls.append(temp_dict)
            for k,v in play.noneCentralCurrencyPlayInfoDTOEnumMap.__dict__.items():
                if '__' not in k:
                    if v.status == play_status:
                        temp_dict = {"gameId":str(self.gameId),
                                      "reason":reason,"currencyPlayId":v.id}
                        params_ls.append(temp_dict)
        params = json.dumps(params_ls,indent=4)
        # print('请求参数\n',params)
        return params

    def get_accept_params(self):
        """获取 管理员待审核 请求参数"""
        params_ls = []
        # r = self.session.get(self.pending_review_path%self.gameId,
        #                      headers=self.headers).text

        r = self.ev_obj.public_send_request(
            api_m.pending_review%self.gameId).text

        res_dict_ls = json.loads(r,encoding='utf-8')
        for res_dict in res_dict_ls:
            params_ls.append(res_dict['id'])
        params = json.dumps(params_ls,indent=4)
        # print('请求参数\n',params)
        return params

    def get_submit_review_params(self,play_status=None):
        """获取提交审核请求参数"""
        self._get_game_text()
        playInfoDTOS=self.game_text['playInfoDTOS']
        params = []
        for play in playInfoDTOS:
            temp={}
            temp['playId']=play['playId']
            temp['centralCurrencyPlayInfoDTOEnumMap']={}
            temp['noneCentralCurrencyPlayInfoDTOEnumMap'] = {}
            for key,value in play['centralCurrencyPlayInfoDTOEnumMap'].items():
                if play_status != None:
                    if value['status'] != play_status:
                        continue
                currency_temp_dict = {}
                currency_temp_dict['id']=value['id']
                temp['centralCurrencyPlayInfoDTOEnumMap'][key]=currency_temp_dict
            for key,value in play['noneCentralCurrencyPlayInfoDTOEnumMap'].items():
                if play_status != None:
                    if value['status'] != play_status:
                        continue
                currency_temp_dict = {}
                currency_temp_dict['id']=value['id']
                try :
                    temp['noneCentralCurrencyPlayInfoDTOEnumMap'][key]=currency_temp_dict
                except:
                    pass

            params.append(temp)
        # print(json.dumps(params,indent=4))
        return  json.dumps(params,indent=4)
        # return params

    @check_step_is_success('预测发布--提交审核')
    def submit_review(self,play_status=None):
        """预测发布--提交审核"""
        parmas = self.get_submit_review_params(play_status=play_status)
        # r = self.session.put(self.submit_review_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.submit_review,parmas).text
        return self._get_reponse_result(r,p_v.STEP_submit_review)


    @check_step_is_success('预测发布--审核通过')
    def pending_deployment_review(self,play_status=None):
        """预测发布--审核通过"""
        parmas = self.get_submit_review_params(play_status=play_status)
        # r = self.session.put(self.pending_deployment_review_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.pending_deployment_review,parmas).text

        return self._get_reponse_result(r,p_v.STEP_pending_deployment_review)


    @check_step_is_success('预测发布--部署')
    def deployment_review(self,play_status=None):
        """预测发布--部署"""

        parmas = self.get_submit_review_params(play_status=play_status)
        # r = self.session.put(self.deployment_review_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.deployment_review,parmas).text

        return self._get_reponse_result(r,p_v.STEP_deployment_review)


    @check_step_is_success('预测管理--预测中--修改抽水')
    def modify_shrink(self,gameId='',playId='',newValue='10',
                      reason='全局抽水修改',modify_currency=[]):
        """修改抽水"""
        res_ls = self.ev_obj.db.get_play_currency_play_and_optionId(gameId,playId)
        self.gameId = gameId
        params = []
        for res in res_ls:
            currency = res[2]
            if len(modify_currency)>0:
                if currency not in str(modify_currency):
                    continue
            params.append({"gameId":gameId,"currencyPlayId":res[0],
                           "currencyOptionId":res[1],
                        "newValue":str(newValue),"reason":reason})

        params = str(json.dumps(params,indent=4,ensure_ascii=False))
        # print('请求参数\n',params)
        # r = self.session.put(self.modify_shrink_path,
        #                      data=params.encode(),headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.modify_shrink,params).text
        print('响应数据：',r)
        return self._get_reponse_result(r,p_v.STEP_award,is_check_db=False)


    @check_step_is_success('预测发布--发布')
    def publish_review(self,play_status=None):
        """预测发布--发布"""
        parmas = self.get_submit_review_params(play_status=play_status)

        # r = self.session.put(self.publish_review_path%self.gameId,
        #                      data=parmas,headers=self.headers).text

        r = self.ev_obj.public_send_request(
            api_m.publish_review%self.gameId,parmas).text
        return self._get_reponse_result(r,p_v.STEP_publish_review)


    @check_step_is_success('预测发布--废弃')
    def discard(self,play_status=None):
        """预测发布--废弃"""
        parmas = self.get_submit_review_params(play_status=play_status)
        # r = self.session.put(self.dicard_path%self.gameId,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(
            api_m.dicard_path%self.gameId,parmas).text
        if len(r)>1:
            return {'text':r,'success':False}
        return {'text':r,'success':True}

    @check_step_is_success('封盘')
    def close(self):
        """封盘"""
        self._get_game_text()
        parmas = self.get_close_params()
        # r = self.session.put(self.close_path,
        #                      data=parmas,headers=self.headers).text

        r = self.ev_obj.public_send_request(api_m.close,parmas).text

        return self._get_reponse_result(r,p_v.STEP_close)


    @check_step_is_success('撤盘')
    def revoke(self):
        """撤盘"""
        parmas = self.get_close_params()
        # r = self.session.put(self.revoke_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.revoke,parmas).text
        if len(r)>1:
            return {'text':r,'success':False}
        return {'text':r,'success':True}

    @check_step_is_success('审核通过')
    def accept(self,is_check_db=True):
        """预测管理--管理员待审核--审核通过"""
        parmas = self.get_accept_params()
        # r = self.session.put(self.accept_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.accept,parmas).text

        return self._get_reponse_result(r,p_v.STEP_accept,is_check_db=is_check_db)


    @check_step_is_success('预测管理--封盘--设置比分')
    def set_game_score(self,score):
        """预测管理--封盘--设置比分"""
        parmas = '{"gameId":"%s","score":"%s"}'%(self.gameId,score)
        # r = self.session.post(self.result_path,
        #                      data=parmas,headers=self.headers).text
        r = self.ev_obj.public_send_request(api_m.set_score,parmas).text

        self.set_option_award_result(score)

        return p_m.get_public_response(r)


    @check_step_is_success('预测管理--已封盘--修改获胜选项')
    def modify_award_option(self,win_index=0,reason='auto_test'):
        """修改获胜选项
        1.获胜选项统一为第一个选项
        2.返回开奖请求参数
        """
        win_option_id_dict = {} #获胜选项
        game_play_info_ls = self.get_game_info()
        for p in game_play_info_ls:
            # p = GameBean()
            win_option_id = p.optionsId_ls[win_index]
            win_option_id_dict[win_option_id] = win_option_id
            params = '{"gameId":%s,"playId":%s,"newValue":%s,"reason":"%s","winCurrencyOptionId":[%s]}' \
                     ''%(self.gameId,p.playId,win_option_id,reason,win_option_id)
            r = self.ev_obj.public_send_request(api_m.modify_award_option,params).text
            print('响应数据',p.playId,r)

            ##设置比赛option结果 赢或输
            for optionId in p.optionsId_ls:
                # option_obj = OptionInfo()
                option_obj = self.options_info_dict[optionId]
                if optionId == win_option_id:
                    option_obj.award_status = BONUS_AWARD
                else:
                    option_obj.award_status = BONUS_LOST

        #设置option获胜结果
        print('获胜选项',win_option_id_dict)
        self.set_option_award_result(win_option_id_dict=win_option_id_dict)

        # return self._get_reponse_result(r,is_only_rereturn_res=True)

    @check_step_is_success('结算管理--结算中--修改非比分赛果')
    def save_win_option_check(self,win_index=0):

        win_option_id_dict = {} #获胜选项
        game_play_info_ls = self.get_game_info()
        params_dict = {'gameId':self.gameId}
        params_ls = []

        commit_params_dict = {'checked':True,'gameId':str(self.gameId)}
        win_options_ls = []

        for p in game_play_info_ls:
            # p = GameBean()
            if p.is_not_score_play() != True:
                continue
            win_option_id = p.optionsId_ls[win_index]
            win_option_id_dict[win_option_id] = win_option_id
            temp_params_dict = {"optionId":win_option_id,"playId":p.playId,"bonusType":"AWARD"}
            temp_commit_dict = {"optionId":win_option_id,"playId":p.playId,"bonusType":"AWARD"}
            params_ls.append(temp_params_dict)
            win_options_ls.append(temp_commit_dict)
        params_dict['options']=params_ls
        params = json.dumps(params_dict,ensure_ascii=False)
        r = self.ev_obj.public_send_request(api_m.save_win_option_check,params).text
        print('修改获胜选项响应数据',r)

        self.set_option_award_result(win_option_id_dict=win_option_id_dict)

        commit_params_dict['optionAward']={'options':win_options_ls}
        params = json.dumps(commit_params_dict,ensure_ascii=False)
        r = self.ev_obj.public_send_request(api_m.commit_result,params).text
        print('提交初审响应数据',r)

        r = self.ev_obj.public_send_request(api_m.calc_game,params).text
        print('计算盈亏响应数据',r)

    @check_step_is_success('结算管理--结算中--提交初验')
    def commit_result(self,score=''):
        if score != '':
            params = '{"gameId":"%s","checked":true,"scoreAward":{"score":"%s","checked":true}}'\
                    %(self.gameId,score)
            r = self.ev_obj.public_send_request(api_m.commit_result,params).text
            print('提交初审响应数据',r)





    @check_step_is_success('结算管理--结算中--修改比分赛果')
    def save_score_check(self,score):
        params = '{"gameId":%s,"score":"%s","checked":true}'%(self.gameId,score)
        r = self.ev_obj.public_send_request(api_m.save_win_option_check,params).text
        print('响应数据',r)
        self.set_option_award_result(score)
        self.commit_result(score)


    @check_step_is_success('预测管理--已封盘--开奖')
    def award(self):
        """预测管理--已封盘--开奖"""
        parmas = self._get_award_request_params()
        # r = self.session.put(self.award_path,
        #                      data=parmas,headers=self.headers).text

        r = self.ev_obj.public_send_request(api_m.award,parmas).text

        return self._get_reponse_result(r,p_v.STEP_award)

    @check_step_is_success('结算管理--待开奖--直接开奖')
    def calc_award(self,score):
        params_dict = {'gameId':str(self.gameId),'checked':True}
        score_award_dict = {'score':score,'checked':True}
        if self.is_all_score_plays:
            #比分玩法
            params_dict['scoreAward'] = score_award_dict
        else:
            #非比分玩法  或  混合玩法(比分玩法和非比分玩法)
            options_ls = []
            for optionId,o in self.options_info_dict.items():
                # option = OptionInfo()
                option = o
                if option.is_not_score_play_attr:
                    #如果是非比分玩法
                    if option.is_win_option():
                        option_dict = {"playId":option.playId,
                                "optionId":option.optionId,"bonusType":option.award_status}
                        options_ls.append(option_dict)
                else:
                    params_dict['scoreAward'] = score_award_dict
            if len(options_ls)>0:
                params_dict['optionAward'] = {'options':options_ls}

        parmas = json.dumps(params_dict,ensure_ascii=False)

        r = self.ev_obj.public_send_request(api_m.calc_award,parmas).text
        print('直接开奖响应数据',r)
        return self._get_reponse_result(r,p_v.STEP_award)

    @check_step_is_success('预测管理--自定义创建--预测中--修改抽水')
    def modify_odds(self,newValue='2.1',reason='auto_test'):
        params = []
        for k,option_info in self.options_info_dict.items():
            # option_info = OptionInfo()
            temp_dict = {}
            temp_dict['gameId'] = self.gameId
            temp_dict['playId'] = option_info.playId
            temp_dict['optionId'] = option_info.optionId
            temp_dict['newValue'] = newValue
            temp_dict['reason'] = reason
            params.append(temp_dict)

        parmas = json.dumps(params,ensure_ascii=False)

        r = self.ev_obj.public_send_request(api_m.modify_odds,parmas).text

        return self._get_reponse_result(r,p_v.STEP_award,is_check_db=False)


    def get_game_info(self):
        plays = self.game_text['playInfoDTOS']
        game_play_info_ls = []
        for play in plays:
            game_bean = PlayBean()
            try:
                game_bean.play_name = play['playName']['zh']
            except:
                game_bean.play_name = ''
            game_bean.market = play['market']
            game_bean.gameId=self.gameId
            game_bean.handicap = play['handicap']
            game_bean.playId=play['playId']
            game_bean.play_option_num = len(play['optionInfoList'])
            central_currency_playId_dict = play['centralCurrencyPlayInfoDTOEnumMap']
            none_central_currency_playId_dict = play['noneCentralCurrencyPlayInfoDTOEnumMap']
            temp_option_dict = {}
            for option in play['optionInfoList']:
                game_bean.optionsId_ls.append(option['optionId'])
                temp_currency_ls = []
                for centralCurrency,value in option['centralCurrencyOptionDTOEnumMap'].items():
                    currency_playId = central_currency_playId_dict[centralCurrency]['id']
                    temp_currency_ls.append([currency_playId,value['id'],centralCurrency,0])

                for none_centralCurrency,value in option['noneCentralCurrencyOptionDTOEnumMap'].items():
                    currency_playId = none_central_currency_playId_dict[none_centralCurrency]['id']
                    temp_currency_ls.append([currency_playId,value['id'],none_centralCurrency,1])
                temp_option_dict[option['optionId']]=temp_currency_ls
                game_bean.options_currencyInfo_dict.update(temp_option_dict)

            game_play_info_ls.append(game_bean)
        return game_play_info_ls

    def check_game_currency_play_status(self,response,run_step_name):
        """检查ortune_currency_play_info 的status"""
     #    self._get_game_play_status_by_step_name(run_step_name)
    #
     #    sql = '''SELECT c_p_i.play_id,c_p_i.`status`,c_p_i.currency from fortune_base_play_info b_p_i,fortune_currency_play_info c_p_i
	# WHERE b_p_i.play_id=c_p_i.play_id and b_p_i.game_id=%s;'''%self.gameId
    #
     #    act_status = ''
     #    result = ''
     #    if response['success']:
     #        act_status = self.ev_obj.game_play_new_status
     #    else:
     #        act_status = self.ev_obj.game_play_old_status
     #    status_ls = self.ev_obj.db.mysqlinfo.selectInfo(sql)
     #    for status in status_ls:
     #        if act_status not in str(status):
     #            result += '\n数据库状态不正确(期望值：%s 实际值：%s)'%(act_status,str(status))
     #    response['text']=response['text']+result
     #    if result != '':
     #        response['success'] = False

        # return response

    def _get_game_play_status_by_step_name(self,run_step_name):
        """通过操作步骤名称获取玩法状态"""
        if run_step_name == p_v.STEP_submit_review: #提交审核
            self.ev_obj.game_play_old_status = p_v.PENDING_SUBMISSION
            self.ev_obj.game_play_new_status = p_v.PENDING_REVIEW

        elif run_step_name == p_v.STEP_pending_deployment_review: #通过审核
            self.ev_obj.game_play_old_status = p_v.PENDING_REVIEW
            self.ev_obj.game_play_new_status = p_v.PENDING_DEPLOYMENT

        elif run_step_name == p_v.STEP_deployment_review: #部署
            self.ev_obj.game_play_old_status = p_v.PENDING_DEPLOYMENT
            self.ev_obj.game_play_new_status = p_v.PENDING_RELEASE

        elif run_step_name == p_v.STEP_publish_review: #发布
            self.ev_obj.game_play_old_status = p_v.PENDING_RELEASE
            self.ev_obj.game_play_new_status = p_v.IN_PREDICTION

        elif run_step_name == p_v.STEP_close: #封盘
            self.ev_obj.game_play_old_status = p_v.IN_PREDICTION
            self.ev_obj.game_play_new_status = p_v.IN_PREDICTION
            self.ev_obj.pre_run_step_name = p_v.STEP_close

        elif run_step_name == p_v.STEP_accept: #管理员待审核
            self.ev_obj.game_play_old_status = self.ev_obj.game_play_new_status
            if self.ev_obj.pre_run_step_name == p_v.STEP_close:
                self.ev_obj.game_play_new_status = p_v.CLOSED
            elif self.ev_obj.pre_run_step_name == p_v.STEP_award:
                self.ev_obj.game_play_new_status = p_v.AWARDING

        elif run_step_name == p_v.STEP_award: #开奖
            self.ev_obj.game_play_old_status = p_v.CLOSED
            self.ev_obj.game_play_new_status = p_v.CLOSED
            self.ev_obj.pre_run_step_name = p_v.STEP_award

    def _get_reponse_result(self,respnse,step_name,is_only_rereturn_res=False
            ,is_go_on=False,is_check_db=True):
        if is_check_db:
            r = respnse
            request_result = {'text':r,'success':True,p_v.is_go_on:is_go_on}
            if len(r)>1:
                request_result['success'] = False
            if is_only_rereturn_res == False:
                request_result = self.check_game_currency_play_status(request_result,step_name)
            return request_result


    def award_all_inprediction_games(self,is_third_game=True):
        """把预测中所有的game 开奖"""
        games = []

        useApi = 'false'
        if is_third_game:
            useApi = 'true'
        r = self.ev_obj.public_send_request(
            api_m.in_prediction_games%(useApi)).text
        r_dict = json.loads(r,encoding='utf-8')
        for l in r_dict['list']:
            games.append(l['gameId'])
        for gameId in games:
            self.set_gameId(gameId)
            self.close()
            self.accept()
            self.modify_award_option()
            self.award()
            self.accept()
        next_page = r_dict['nextPage']
        if next_page > 0:
            self.award_all_inprediction_games(is_third_game)
        else:
            return

    @check_step_is_success('设置比赛结果后  计算盈亏')
    def fetch_game_amount(self,score=None):
        """计算盈亏"""
        exp_dict = {} #key=currency_play_id, value=coin.game.dataBean.CalcGameAmout
        params_ls = []
        temp_currency_play_id_dict = {}
        for optionId,o in self.options_info_dict.items():
            # o = OptionInfo()
            # option = o
            logger.info('选项%s 比赛结果：%s'%(o.optionId,o.award_status))
            if o.is_win_option():
                #获取currency_play_id
                sql = w_sql.currency_play_and_option_ids_by_optionId%o.optionId
                sql_res_ls = self.ev_obj.db.public_query_info(sql)
                for sql_res in sql_res_ls:
                    currency_play_id = sql_res[0]
                    currency_option_id = sql_res[1]
                    if exp_dict.get(currency_play_id) != None:
                        v = exp_dict.get(currency_play_id)
                        v.currency_option_id_ls.append(currency_option_id)
                    else:
                        game_amout_obj = CalcGameAmout(currency_play_id)
                        game_amout_obj.currency_option_id_ls.append(currency_option_id)
                        game_amout_obj.currency = sql_res[2]
                        game_amout_obj.play_id = o.playId
                        exp_dict[currency_play_id] = game_amout_obj

                    if temp_currency_play_id_dict.get(currency_play_id) != None:
                        params = temp_currency_play_id_dict.get(currency_play_id)
                        options_obj = {"currencyOptionId":currency_option_id,"bonusType":o.award_status}
                        params['options'].append(options_obj)
                    else:
                        params = {"currencyPlayId":-1,"options":[{"currencyOptionId":-1,"bonusType":o.award_status}],"score":"1:0"}
                        params['score'] = score
                        params['currencyPlayId'] = currency_play_id
                        params['options'][0]['currencyOptionId'] = currency_option_id
                    temp_currency_play_id_dict[currency_play_id]=params
        for k,v in temp_currency_play_id_dict.items():
            params_ls.append(v)

        params = json.dumps(params_ls,ensure_ascii=True,indent=4)
        r = self.ev_obj.public_send_request(api_m.fetch_game_amount,params).text
        act_ls = json.loads(r,encoding='utf-8')


        for act_dict in act_ls:
            currency = act_dict['currency']
            currency_play_id = act_dict['currencyPlayId']
            if currency_play_id == 25066:
                print(13)
            act_period_total = act_dict['periodTotal']
            exp_obj = exp_dict[currency_play_id]
            exp_obj.get_exp_game_amout(self.ev_obj.db,self.options_info_dict)
            # exp_obj.print_info(act_period_total)
            if act_period_total != exp_obj.game_amout:
                exp_obj.print_info(act_period_total)


        #计算每个币种的总盈亏
        game_total_amout_obj = CalcTotalGameAmout()
        for k,v in exp_dict.items():
            game_total_amout_obj.play_currency_game_amout_obj_ls.append(v)
        game_total_amout_obj.calc_total_game_amout()
        print('每个币种的总盈亏')
        game_total_amout_obj.print_info()






class PlayBean():
    """game信息"""

    def __init__(self):
        self.gameId=0
        self.playId=0
        self.play_option_num = 2 #玩法选项数量
        self.handicap='' #盘口
        self.play_name='' #玩法名称(中文)
        self.market = ''
        self.optionsId_ls=[]
        #key=optionId value=[[currencyPlayId,currency_optionId,currency,central]]
        self.options_currencyInfo_dict={}

        #各选项的获奖状态(key=optionId,value=CANCEL/HALF_WIN/HALF_LOST/DRAW)
        self.option_bonus_type={}

    def get_award_request_params(self,award_options_ls):
        """award_options_ls 为获胜选项"""

        for options in award_options_ls:
            params = '{"gameId":%s,"currencyPlayId":%s,"currencyOptionId":%s}'
            for currencyInfo_ls in self.options_currencyInfo_dict[options]:
                params = params%(self.gameId,)
                pass


    def _set_play_option_result(self,option_result_map):
        for option,result in option_result_map.items():
            pass

    def is_not_score_play(self):
        """是否为比分玩法"""
        if self.market == None:
            return True
        if re.search('Map\d+',self.market) != None:
            # print('非比分玩法：',self.play_name)
            return True
        # print('比分玩法：',self.play_name)
        return False

class OptionInfo():
    """选项信息"""
    optionId = 0
    playId = 0
    tag = 'homeOd' #主队homeOd 或客队 awayOd
    handicap = '' #盘口
    award_status = '' #选项中奖状态
    play_type = '' #玩法类型  play.market
    is_mul_handicap = True #是否是多盘口
    is_not_score_play_attr = False




    def is_not_score_play(self):
        """是否为非比分玩法"""
        if self.play_type == None:
            self.is_not_score_play_attr = True
            return True
        if re.search('Map\d+',self.play_type) != None:
            return True
        return False

    def is_home(self):
        if self.tag == 'homeOd':
            return True
        return  False

    def is_under(self):
        if self.tag == 'underOd':
            return True
        return  False

    def is_win_option(self):
        """是否是获胜选项"""
        if self.is_mul_handicap:
            if self.award_status != BONUS_LOST:
                return True
        else:
            if BONUS_AWARD == self.award_status or BONUS_HALF_WIN== self.award_status:
                return True
        return False


    def print_option_award_result(self):
        """打印选项的获奖情况"""
        print(self.playId,self.play_type,self.optionId,self.tag,self.handicap,self.award_status)


class BettingInfo():
    """投注信息"""

    currency_option_id = 0
    optionId = 0
    address = ''
    odds = 0.0
    amount = 0.0
    user_account = ''
    user_id = ''
    status = ''
    currency = ''
    return_amount = 0.0 #返回给用户的金额

    def set_award_amount(self,option_result_dict):
        """获取开奖后应该  开奖金额"""
        option_obj = option_result_dict[self.optionId]
        # option_obj = OptionInfo()
        status = option_obj.award_status
        if status == BONUS_AWARD:
            self.return_amount = calculate_float_data(self.odds,self.amount,'*')
        elif status == BONUS_HALF_WIN:
            self.return_amount = calculate_float_data(self.odds*self.amount/2
                                        ,self.amount/2,'+')
            # self.return_amount = round(self.odds*self.amount/2+self.amount/2,8)
        elif status == BONUS_CANCEL:
            # self.return_amount = calculate_float_data(self.odds,self.amount,'*')
            self.return_amount = round(self.amount,8)
        elif status == BONUS_HALF_LOST:
            # self.return_amount = calculate_float_data(self.odds,self.amount,'*')
            self.return_amount = round(self.amount/2,8)
        elif status == BONUS_LOST:
            self.return_amount = calculate_float_data(self.odds,self.amount,'*')
            self.return_amount = 0

        # if self.currency == 'USDT':
        #     # print(self.amount,self.odds,self.return_amount)
        #     print('%s	%s	%s'%(self.amount,self.odds,self.return_amount))



class CalcTotalGameAmout():
    """计算每个币种的总盈亏 """

    def __init__(self):
        self.play_currency_game_amout_obj_ls = [] #value = CalcGameAmout

    def calc_total_game_amout(self):
        """计算每个币种的总投注"""
        self.total_game_amout_dict = {} #key=currency value=CalcGameAmout()
        for game_amout_obj in self.play_currency_game_amout_obj_ls:
            # game_amout_obj = CalcGameAmout()
            temp_obj = self.total_game_amout_dict.get(game_amout_obj.currency)
            if temp_obj == None:
                self.total_game_amout_dict[game_amout_obj.currency] = game_amout_obj
            else:
                # temp = CalcGameAmout()
                temp = self.total_game_amout_dict[game_amout_obj.currency]
                # temp.return_amount = temp.return_amount+game_amout_obj.return_amount
                # temp.game_amout = temp.game_amout + game_amout_obj.game_amout
                # temp.total_bet_amout = temp.total_bet_amout + game_amout_obj.total_bet_amout
                temp.return_amount = calculate_float_data(temp.return_amount,game_amout_obj.return_amount,'+')
                temp.game_amout = calculate_float_data(temp.game_amout,game_amout_obj.game_amout,'+')
                temp.total_bet_amout = calculate_float_data(temp.total_bet_amout,game_amout_obj.total_bet_amout,'+')

        print('end')

    def print_info(self):
        for k,v in self.total_game_amout_dict.items():
            v.print_info()



class CalcGameAmout():
    """按玩法计算game的盈亏"""

    def __init__(self,currency_play_id=0):
        self.currency_play_id = currency_play_id
        self.currency_option_id_ls = []
        self.total_bet_amout = 0 #总投注
        self.return_amount  = 0 #返回给用户的金额
        self.game_amout = 0 #盈亏金额
        self.currency = ''
        self.play_id = ''
        pass

    def get_exp_game_amout(self,db,options_info_dict):
        """计算盈亏期望值"""
        b = BettingInfo()
        res = db.get_betting_info_obj_ls(self.currency_play_id)
        if len(res) > 0:
            for r in res:
                # b = res[0]
                b = r
                b.set_award_amount(options_info_dict)
                # self.return_amount += b.return_amount
                self.return_amount = calculate_float_data(self.return_amount,b.return_amount,'+')

        #获取总投
        self.total_bet_amout = 0

        res = db.public_query_info(w_sql.all_bet_amount_by_currency_play_id%self.currency_play_id)
        if res[0][0] != None:
            self.total_bet_amout = float(res[0][0])
        self.game_amout = calculate_float_data(self.total_bet_amout,self.return_amount,'-')

    def print_info(self,act_value=''):
        str_info = 'play_id:%s,currency:%s,currency_play_id:%s,盈亏：(期望值 %s 实际值 %s),总投注：%s,返回给用户金额：%s'%\
              (self.play_id,self.currency,self.currency_play_id,
               self.game_amout,act_value,self.total_bet_amout,self.return_amount)
        print(str_info)
        return  str_info





# if __name__ == '__main__':
#     o = GamePublicRequest('api.intranet.etcgame.com','testing',False)
#     o.login_register.login()
    # game_info = GameBean(60,headers=o.login_register.headers,testUrl=o.login_register.testUrl)





