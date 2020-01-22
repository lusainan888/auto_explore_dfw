#coding=utf-8
import requests
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from coingame.beans.coinGameBeans import GameBean,OptionInfo, BettingInfo
from coingame.beans.create_data import CreateLsportsMockData
from coingame.beans.dataBean import Categories, UserAcctBalanceInfo, EventInfo,OptionsOddsInfo, PlaysOddsInfo,GameOddsInfo

from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.globalparam import get_project_path
from coingame.config.testEnvironmentManager import TestEnvironment
import json
import re
import copy
from coingame.module.oddsUtil import Odds
from coingame.module.decorators import check_step_is_success
from public.common.util import logger, dict_to_obj, create_up_file_data,truncate
from coingame.beans import public_values as p_v
from coingame.beans import public_method as p_m
from coingame.beans import api_request_path_manager as api_m
import time
from coingame.beans import public_values as w_v
from coingame.beans import sql_manager as w_sql
from coingame.beans import lsports_public_values as w_lsport_v

class GamePublicRequest():
    def __init__(self,domain=None,testEv=None,isCrm=True,http='http'):
        self.ev_obj = TestEnvironment(domain,testEv,isCrm=True,http=http)
        self.login_and_register = GameLoginAndRegister(self.ev_obj)
        self.create_game_info = CreateGameInfo(self.ev_obj)
        self.new_create_game_info = NewCreateGameInfo(self.ev_obj)
        self.game_bean = GameBean(self.ev_obj)
        self.website = WebSiteLogic(self.ev_obj)
        self.award = Award(self.ev_obj)
        self.check = CheckData(self.ev_obj)
        self.odds_obj = Odds(self.ev_obj)
        self.crm = CRMLogic(self.ev_obj)
        self.create_lsports_mock_data_obj = CreateLsportsMockData(self.ev_obj)



        for k,v in self.ev_obj.__dict__.items():
            setattr(self,k,v)


    def set_other_objs_headers(self,headers):
        """设置其它对象的headers"""
        setattr(self.ev_obj,'headers',headers)

    def get_gameIds(self,eventId=None,is_third=True,
                    game_status='PENDING_SUBMISSION',index=None):
        """在预测发布--待提交页--获取gameId
        game_status:PENDING_SUBMISSION(待提交)/PENDING_RELEASE(待发布)
        """
        if eventId != None:
            return self.ev_obj.db.get_gameId(eventId)
        else:
            url = self.testUrl+'/games/status/%s?useApi=false&pageNum=1'%game_status
            if is_third:
                url = self.testUrl+'/games/status/%s?useApi=true&pageNum=1'%game_status
            r = self.session.get(url,headers=self.headers).text
            res_dict = json.loads(r)
            result = []
            for game in res_dict['list']:
                result.append(game['gameId'])
            if index != None:
                return result[index]
            return result

    @check_step_is_success('用户投注')
    def users_betting(self,betting_users_and_params_dict):
        """用户投注"""
        result = ''
        betting_users_ls = betting_users_and_params_dict['users']
        betting_params_ls = betting_users_and_params_dict['betting_params']
        usdt_amout_dict = []
        for user in betting_users_ls:
            userId = self.db.get_userId(user['user_name'])
            self.login_and_register.login(user['user_name'],user['user_password'])

            all_amout = 0

            for params in betting_params_ls:
                betting_result = self.website.betting(params,userId=user['user_name'])
                # result += self.check.check_after_betting_dbinfo(params,betting_result,userId)
                # amout = 0
                # if 'SUCCESS' in str(betting_result):
                #     temp_dict = json.loads(params,encoding='utf-8')
                #     currency = temp_dict['currency']
                #     if currency=='TRON':
                #         currency = 'TRX'
                #
                #     for record in temp_dict['records']:
                #         amout += float(record['amount'])
                #
                #     url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE' \
                #         '&from_currency=%s&to_currency=USDT&apikey=PP0XZ09T6D0HXQ3L'%currency
                #     try:
                #         time.sleep(22)
                #         text = self.ev_obj.session.get(url).text
                #         text_dict = json.loads(text,encoding='utf-8')
                #
                #         rate = float(text_dict['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                #         all_amout += amout * rate
                #     except:
                #         print(url)

                    # usdt_amout_dict.append('%s:%s'%())
            # usdt_amout_dict.append('%s:%s'%())
            # print('富豪傍投注：%s:%s'%(user['user_name'],all_amout))




        if result == '':
            return {'text':result,'success':True,p_v.is_go_on:True}
        else:
            return {'text':result,'success':False,p_v.is_go_on:True}





class WebSiteLogic():
    """前端类"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

    @check_step_is_success('投注')
    def betting(self,betParmas,userId=''):
        """投注"""
        currency_options_ls = []
        # if isinstance(betParmas,dict) == False:
        #     betParmas = json.loads(betParmas,encoding=w_v.ENCODING)
        # for record in betParmas['records']:
        #     sql_res = self.ev_obj.db.public_query_info(w_sql.final_odds%record['currencyOptionId'])
        #     final_odds = float(sql_res[0][0])
        #     record['odds'] = final_odds

        betParmas = json.dumps(betParmas)

        r = self.ev_obj.public_send_request(api_m.betting,betParmas).text
        logger.info('投注请求参数：%s'%betParmas)
        # logger.info('投注响应数据：%s'%r.text)
        return p_m.get_public_response(r,other_text='投注用户(%s) 投注请求参数：%s'
                        %(userId,betParmas),is_go_on=True,run_success_text='SUCCESS')



class CRMLogic():
    """CRM 其它请求"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

    @check_step_is_success('增加或修改队伍基础数据库')
    def add_or_edit(self,sport_type=w_v.sport_soccer,create_num=60):
        participantId = w_v.sport_league_dict[sport_type]*w_v.participant_start_index

        start_index = w_v.participant_start_base_id
        temp_name = '%s_%s'
        icon_url = self.dirtree_image_upload()
        temp_betParmas = '{"participantId":"%s","cronUrl":"%s","cronSmallUrl":"%s",' \
                    '"zh":"%s","en":"%s","ko":"%s",' \
                    '"ja":"%s","zhHant":"%s","sport":"%s"}'
        for i in range(create_num):
            index = participantId+start_index+i
            name = temp_name%(sport_type,start_index+i)
            betParmas = temp_betParmas%(index,icon_url,icon_url,name,name,name,name,name,sport_type.upper())
            r = self.ev_obj.public_send_request(api_m.add_or_edit,betParmas).text
            logger.info('增加队伍(id=%s)基础数据响应数据：%s'%(index,r))



    @check_step_is_success('上传目录树图片')
    def dirtree_image_upload(self,file=w_v.icon_path+'1.png'):

        body = create_up_file_data(file,boundary=w_v.boundary)
        #
        # r = self.ev_obj.public_send_request(api_m.dirtree_image_upload
        #                     ,data=body,content_type=w_v.upimage_content_type).text

        body = create_up_file_data(file,boundary=w_v.boundary)

        file_dict = {'file': ("1.png", open(file, 'rb'), "image/png")}

        r = self.ev_obj.public_send_request(api_m.dirtree_image_upload
                            ,file_dict=file_dict,content_type=w_v.upimage_content_type).text

        logger.info('上传图片响应数据：%s'%r)
        return r



    @check_step_is_success('创建目录树')
    def create_categories(self,league,sport_type,icon_name='1.png'):
        #获取parent_id
        parent_id = self.ev_obj.db.public_query_info(
            w_sql.sport_id.replace('{var}',sport_type),1)

        params = {"nameMap":{"zh":"auto_test","en":"auto_test","ja":"auto_test","ko":"auto_test","ru":"auto_test","zh-Hant":"auto_test","vi":"auto_test"}
            ,"source":None,"sport":None,"league":str(league),"color":"WHITE","icon":"","parentId":parent_id}

        params['icon'] = self.dirtree_image_upload()
        params = json.dumps(params,ensure_ascii=False)
        r = self.ev_obj.public_send_request(api_m.create_categories,
                                data=params).text

        logger.info('创建目录树响应数据：%s'%r)
        return r


class CheckData():
    """检查数据类"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)


    def check_after_betting_dbinfo(self,betting_params,betting_request_result,userId):
        """检查投注后数据库信息"""
        result = ''
        betting_dict = json.loads(betting_params,encoding='utf-8')
        betting_info_dict_ls = betting_dict['records']
        currency = betting_dict['currency']
        for betting_info_dict  in betting_info_dict_ls:
            currency_optionid = betting_info_dict['currencyOptionId']
            amount = betting_info_dict['amount']
            betting_info_ls = self.db.get_betting_info_by_currency_optionId(currency_optionid,userId)
            request_result = betting_request_result['success']
            act_res = str(betting_info_ls)
            if request_result:
                #投注成功
                exp_res = ".*%s.*, '%s', %s.*"%(amount,currency,currency_optionid)
                if re.search(exp_res,act_res) == None or len(betting_info_ls)>1:
                    result += '期望值：%s  实际值：%s\n'%(exp_res,act_res)
            else:
                #投注失败
                if len(betting_info_ls) > 0:
                    result += '投注失败但是数据（%s）保存成功\n'%(act_res)
        if result != '':
            result = '投注后数据库信息不正确：\n'+result
        return result



class CreateGameInfo():
    """创建标题类"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

        #key=sport 例ESPORTS：电竞  Basketball:篮球 value=map(key=league value=Categories类对象)
        self.categories={}



    def _get_category_info(self):
        if len(self.categories) == 0:
            r = self.ev_obj.public_send_request(api_m.categories).text
            dicts_ls = json.loads(r,encoding='utf8')
            leidata_dict=None
            for d in dicts_ls:
                for level2 in d['subNodes']:
                    subNodes_dict = {}
                    for level3 in level2['subNodes']:
                        category_obj = Categories()
                        category_obj.id = d['id']
                        category_obj.source=level2['source']
                        category_obj.sport=level2['sport']
                        category_obj.level_1_name=d['name']
                        category_obj.level_2_name=level2['name']
                        category_obj.level_3_name=level3['name']
                        category_obj.categoryId=level3['id']
                        for level4 in level3['subNodes']:
                            level4_category_obj = copy.deepcopy(category_obj)
                            level4_category_obj.level_4_name = level4['name']
                            category_obj.league=level4['league']
                            subNodes_dict[category_obj.league]=level4_category_obj
                        category_obj.league=level3['league']
                        subNodes_dict[category_obj.league]=category_obj
                    if self.categories.get(level2['sport']) == None:
                        self.categories[level2['sport']] = subNodes_dict
                    else:
                        self.categories[level2['sport']].update(subNodes_dict)

    def auto_create_funny(self,optionNum=2,categoryId=38,pre_zh_name='Auto_test_',
                          noneCenralCurrency_ls=['ETH','ETC'],
                          not_contains_currency_ls=[]):
        """
        自动创建趣味竞猜
        optionNum:需要创建几个选项
        noneCenralCurrency_ls:指定需要创建的非中心化的币种
        """
        path = get_project_path()+'/coinGame/data/coingame/'
        file_path = path+'funny_name_index.txt'
        text = open(file_path).read()
        temp_dict = json.loads(text,encoding='utf-8')
        index = temp_dict.get(self.testEv)
        if index == None:
            index = 1
        temp_dict[self.testEv]=1+index
        json.dump(temp_dict,open(file_path,'w'),ensure_ascii=False,indent=4)

        zh_name='%s_%s_LTEST%s'%(pre_zh_name,optionNum,index)
        file_path = path+'funny_template.txt'
        template_dict = json.load(open(file_path,'r',encoding='utf-8'))

        c_o_dict = template_dict['playInfoDTOS'][0]['optionInfoList'][0]['centralCurrencyOptionDTOEnumMap']
        c_p_dict = template_dict['playInfoDTOS'][0]['centralCurrencyPlayInfoDTOEnumMap']
        for currency in not_contains_currency_ls:
            c_p_dict.pop(currency)
            c_o_dict.pop(currency)

        for noneCenralCurrency in noneCenralCurrency_ls:
            template_dict['playInfoDTOS'][0]['optionInfoList'][0].setdefault('noneCentralCurrencyOptionDTOEnumMap', {})
            template_dict['playInfoDTOS'][0].setdefault('noneCentralCurrencyPlayInfoDTOEnumMap', {})
            template_dict['playInfoDTOS'][0]['optionInfoList'][0]['noneCentralCurrencyOptionDTOEnumMap']\
                [noneCenralCurrency]={'betCap':'400','shrink':0.01}
            template_dict['playInfoDTOS'][0]['noneCentralCurrencyPlayInfoDTOEnumMap']\
                [noneCenralCurrency]={'betCap':'400'}

        template_dict['gameTitle']['zh']=zh_name
        template_dict['gameDescribe']['zh']=zh_name
        template_dict['categoryId']=categoryId
        for i in range(1,optionNum):
            temp_option = copy.deepcopy(template_dict['playInfoDTOS'][0]['optionInfoList'][0])
            for k in temp_option['optionName']:
                temp_option['optionName'][k]=str(i+1)
            originalOdds = float(temp_option['originalOdds'])+i
            temp_option['originalOdds'] = originalOdds
            template_dict['playInfoDTOS'][0]['optionInfoList'].append(temp_option)


        params = json.dumps(template_dict,indent=4)
        # print('请求参数：',params)
        url = self.testUrl+'/games/'
        r = self.session.post(url,data=params.encode('utf-8'),headers=self.headers)
        if r.text == '':
            print('创建成功',r.text)
        else:
            print('创建失败',r.text)

    @check_step_is_success('创建第三方数据比赛')
    def create_third_game(self,sport,noneCenralCurrency_ls=['ETC','ETH']
            ,league='',eventId='',is_get_not_score_play=False,
            case_data_obj=None):
        """第三方数据创建
        sport = Soccer/Basketball/Tennis/ESPORTS
        步骤：
        1.获取种类信息
        2.根据sport获取map key=league value=Categories
        3.根据sport league获取比赛eventId 和比赛名称
        4.过滤掉无效的eventIds
        5.发送请求 获取templates
        6.创建请求参数
        7.发送创建game请求(如果提示 比赛已经存在 则保存该无效的eventId)
        """
        self._get_category_info()
        league_map = self.categories[sport]
        if league == '':
            return  self._create_third_game(sport,noneCenralCurrency_ls,is_get_not_score_play,case_data_obj)
        else:
            # gameId = self.db.get_gameId(eventId)
            # if gameId != None:
            #     # print('数据库已经存在该比赛了')
            #     return {'text':'数据库已经存在该比赛了','success':False}
            # else:
            category = league_map[league]
            eventId_vs_ls = self._get_eventId_vs_ls(sport,league)
            for eventId_vs in eventId_vs_ls:

                eventId = eventId_vs[0]
                print('eventId',eventId)
                gameId = self.db.get_gameId(eventId)
                if gameId != None:
                    logger.info('比赛已经存在(gameId=%s)：%s'%(gameId,str(eventId_vs)))
                if gameId == None:
                    text = self._get_templates_response(eventId,category.categoryId,sport,
                                                        league,category.source)
                    if text != None:
                        params = self._create_create_third_game_parmas(text,noneCenralCurrency_ls)
                        # print('请求参数\n',params)
                        url=self.testUrl+'/games/'
                        r = self.session.post(url,data=params.encode(),headers=self.headers).text
                        if len(r)>0:
                            logger.info('eventId=%s 创建第三方数据响应数据：\n%s'%(eventId,r))
                            # print(eventId,'创建第三方数据响应数据：\n',r)
                        else:
                            # print('创建成功',eventId)
                            logger.info('创建成功：%s'%(eventId))
                            self.ev_obj.game_play_new_status = p_v.PENDING_SUBMISSION #玩法状态为待提交
                            return {'text':eventId,'success':True}
                else:
                    #比赛已存在
                    continue


            return {'text':'league=%s 已无比赛'%league,'success':False,p_v.is_go_on:False}


    @check_step_is_success('lsports_创建第三方数据比赛')
    def create_third_game_lsports(self,sport,noneCenralCurrency_ls=['ETC','ETH']
            ,league='',eventId='',is_get_not_score_play=False,
            case_data_obj=None):
        """第三方数据创建
        sport = Soccer/Basketball/Tennis/ESPORTS
        步骤：
        1.获取种类信息
        2.根据sport获取map key=league value=Categories
        3.根据sport league获取比赛eventId 和比赛名称
        4.过滤掉无效的eventIds
        5.发送请求 获取templates
        6.创建请求参数
        7.发送创建game请求(如果提示 比赛已经存在 则保存该无效的eventId)
        """
        self._get_category_info()
        league_map = self.categories[sport]
        return  self._create_third_game_lsports(sport,noneCenralCurrency_ls,
                is_get_not_score_play,case_data_obj,league_param=league)



    def _create_third_game(self,sport,noneCenralCurrency_ls=['ETC','ETH'],\
                           is_get_not_score_play =False,case_data_obj=None):
        """第三方数据创建
        sport = Soccer/Basketball/Tennis/ESPORTS
        步骤：
        1.获取种类信息
        2.根据sport获取map key=league value=Categories
        3.根据sport league获取比赛eventId 和比赛名称
        4.过滤掉无效的eventIds
        5.发送请求 获取templates
        6.创建请求参数
        7.发送创建game请求(如果提示 比赛已经存在 则保存该无效的eventId)
        """

        self._get_category_info()
        league_map = self.categories[sport]
        is_stop_create = False
        need_remove_league_ls = []
        for league,v in league_map.items():
            eventinfo_ls = self._get_eventId_vs_ls(sport,league)
            # print('test',v.get_levels_name(),len(eventId_vs_ls))
            if len(eventinfo_ls)>0:
                # print(league,eventId_vs_ls)
                print('目录级：',v.get_levels_name(),eventinfo_ls)
            if len(eventinfo_ls) == 0:
                #移除此league
                need_remove_league_ls.append(league)
                continue
            else:
                eventinfo_ls = self._get_valid_eventId_ls(sport,eventinfo_ls,0)
                category = league_map[league]
                # category = Categories()
                for eventId_vs in eventinfo_ls:
                    eventId = eventId_vs[0]
                    gameId = self.db.get_gameId(eventId)
                    if gameId != None:
                        logger.info('比赛已经存在(gameId=%s)：%s'%(gameId,str(eventId_vs)))
                        continue
                    text = self._get_templates_response(eventId,category.categoryId,sport,
                                                league,category.source)

                    if text != None:
                        if self._get_not_score_play(text,is_get_not_score_play=is_get_not_score_play)\
                                == False:
                            continue
                        params = self._create_create_third_game_parmas(text,noneCenralCurrency_ls)
                        # r = self.ev_obj.public_send_request(api_m.games,params).text
                        r = ''
                        if len(r)>0:
                            print(eventId_vs,'创建第三方数据响应数据：\n',r)
                            if '比赛已存在' in r:
                                self._save_invalid_eventId_or_league(sport,eventId_vs[0])
                        else:
                            print('创建成功',eventId_vs)
                            is_stop_create=True
                            self._save_invalid_eventId_or_league(sport,eventId_vs[0])
                            self.ev_obj.game_play_new_status = p_v.PENDING_SUBMISSION #玩法状态为待提交
                            # break
                            # return eventId_vs[0]
                            return {'text':eventId_vs[0],'success':True}
                if is_stop_create:
                    break
        #移除无效的league
        for k in need_remove_league_ls:
            league_map.pop(k)
        return {'text':'无可用比赛可创建','success':False}

    def _create_third_game_lsports(self,sport,noneCenralCurrency_ls=['ETC','ETH'],\
                           is_get_not_score_play =False,case_data_obj=None,
                           league_param=''):
        """第三方数据创建
        sport = Soccer/Basketball/Tennis/ESPORTS
        步骤：
        1.获取种类信息
        2.根据sport获取map key=league value=Categories
        3.根据sport league获取比赛eventId 和比赛名称
        4.过滤掉无效的eventIds
        5.发送请求 获取templates
        6.创建请求参数
        7.发送创建game请求(如果提示 比赛已经存在 则保存该无效的eventId)
        """
        self._get_category_info()
        league_map = self.categories[sport]
        is_stop_create = False
        need_remove_league_ls = []
        for league,v in league_map.items():
            if league_param != '' :
                league = league_param
                v = league_map[league]
                is_stop_create = True
            eventinfo_ls = self._get_event_info_ls(sport,league)
            print('test',v.get_levels_name(),len(eventinfo_ls))
            if len(eventinfo_ls)>0:
                # print(league,eventId_vs_ls)
                print('目录级：',v.get_levels_name(),len(eventinfo_ls))
            if len(eventinfo_ls) == 0:
                continue
            else:
                category = league_map[league]
                # category = Categories()
                for eventId_vs in eventinfo_ls:
                    eventId = eventId_vs.id
                    if self._check_game_is_exist(eventId_vs,sport):
                        continue

                    text = self._get_templates_response(eventId,category.categoryId,sport,
                                                league,category.source)

                    if text != None:
                        if self._get_not_score_play(text,is_get_not_score_play=is_get_not_score_play)\
                                == False:
                            continue
                        params = self._create_create_third_game_parmas(text,noneCenralCurrency_ls,eventId_vs)
                        r = self.ev_obj.public_send_request(api_m.games,params).text
                        # r = ''
                        if len(r)>0:
                            print(eventId_vs,'创建第三方数据响应数据：\n',r)
                        else:
                            print('创建成功',eventId_vs.info())
                            is_stop_create=True
                            self.ev_obj.game_play_new_status = p_v.PENDING_SUBMISSION #玩法状态为待提交
                            return {'text':eventId_vs.id,'success':True}
                if is_stop_create:
                    break

        return {'text':'无可用比赛可创建','success':False}




    def create_third_game_by_need(self,sport,noneCenralCurrency_ls=['ETC','ETH'],\
                           is_get_not_score_play =False,case_data_obj=None):
        """第三方数据创建
        sport = Soccer/Basketball/Tennis/ESPORTS
        步骤：
        1.获取种类信息
        2.根据sport获取map key=league value=Categories
        3.根据sport league获取比赛eventId 和比赛名称
        6.创建请求参数
        """

        self._get_category_info()
        league_map = self.categories[sport]
        is_stop_create = False
        need_remove_league_ls = []
        for league,v in league_map.items():

            eventId_vs_ls = self._get_eventId_vs_ls(sport,league)
            if len(eventId_vs_ls)>0:
                # print(league,eventId_vs_ls)
                # v = Categories()
                print('目录级：',v.get_levels_name(),eventId_vs_ls)
                eventId_vs_ls = self._get_valid_eventId_ls(sport,eventId_vs_ls,0)
                category = league_map[league]
                # category = Categories()
                for eventId_vs in eventId_vs_ls:
                    eventId = eventId_vs[0]
                    if self._save_or_read_eventId(eventId,is_read=True):
                        continue
                    gameId = self.db.get_gameId(eventId)
                    if gameId != None:
                        logger.info('比赛已经存在(gameId=%s)：%s'%(gameId,str(eventId_vs)))
                        continue
                    text = self._get_templates_response(eventId,category.categoryId,sport,
                                                league,category.source)
                    if self._get_not_score_play(text,is_get_not_score_play=is_get_not_score_play)\
                        == False:
                        continue
                    if text != None:
                        is_need_handicap = self._is_need_handicap(text,case_data_obj)
                        print('获取的结果',is_need_handicap)
                        if  is_need_handicap == False:
                            #如果没有找到符合要求的eventId  就保存
                            self._save_or_read_eventId(eventId,is_read=False)

                            temp_result = self.create_third_game_by_need(sport,noneCenralCurrency_ls,\
                           is_get_not_score_play,case_data_obj)
                            if temp_result['success']:
                                return {'text':eventId_vs[0],'success':True}
                        else:
                            params = self._create_create_third_game_parmas(text,noneCenralCurrency_ls)
                            # r = self.ev_obj.public_send_request(api_m.games,params).text
                            r = ''
                            if len(r)>0:
                                print(eventId_vs,'创建第三方数据响应数据：\n',r)
                            else:
                                print('创建成功',eventId_vs)
                                is_stop_create=True
                                self.ev_obj.game_play_new_status = p_v.PENDING_SUBMISSION #玩法状态为待提交

                                return {'text':eventId_vs[0],'success':True}
                if is_stop_create:
                    break

        return {'text':'无可用比赛可创建','success':False}


    def query_can_create_leidata_game(self):
        """查询能够 创建电竞比赛的信息"""
        #读取数据库 查询有比赛 且没有被创建的电竞数据
        sql = """
            SELECT DISTINCT m.tournament_id,m.ref_id from leidata_match m,leidata_odds o where m.ref_id=o.match_id
                and m.suspended=0 and m.status=0 and m.visible=1 and m.start_time>now()
                    and o.suspended=0 and o.status=0 and o.is_live=0 and o.visible=1
                        and m.ref_id not in(SELECT g.outer_event_id from fortune_base_game_info g
                                where g.outer_event_id is not null) ORDER BY m.tournament_id;
        """
        league_eventId_ls = self.mysqlinfo.selectInfo(sql)
        league_eventIds_dict = {}
        for league_eventId in league_eventId_ls:
            try:
                event_ls = league_eventIds_dict[league_eventId[0]]
                event_ls.append(league_eventId[1])
            except:
                league_eventIds_dict[league_eventId[0]]=[league_eventId[1]]
        # print(league_eventId_ls)
        for league in league_eventIds_dict:
            url = self.testUrl+'/bets-api/upcoming-games?sport=ESPORTS&league=%s' \
                               %(league)
            r = self.session.get(url,headers=self.headers).text
            r_ls = json.loads(r,encoding='utf8')
            valid_eventId_ls=league_eventIds_dict[league]
            c = self._get_categoryId_byleague('ESPORTS',league)
            if c != None:
                print(c.get_levels_name(),league)
                for event in valid_eventId_ls:
                    for l in r_ls:
                        if event == l['id']:
                            print('\t',l['id'],l['vs'])
                            break
                # break

    def _get_not_score_play(self,templates_dict=None,is_get_not_score_play=False):
        """是否需要获取非比分玩法 """

        if is_get_not_score_play:
            if type(templates_dict) != dict:
                templates_dict = json.loads(templates_dict,encoding='utf-8')

            plays_0 = templates_dict['plays']
            for play in plays_0:
                for p in play['plays']:
                    market = p['market']
                    if market == None:
                        return True
                    if re.search('Map\d+',market) != None:
                        # print('非比分玩法：',self.play_name)
                        return True
                    # print('比分玩法：',self.play_name)
                    return False
        return True

    # def _get_category_info(self):
    #     if len(self.categories) == 0:
    #         r = self.ev_obj.public_send_request(api_m.categories).text
    #         dicts_ls = json.loads(r,encoding='utf8')
    #         leidata_dict=None
    #         for d in dicts_ls:
    #             subNodes_dict = {}
    #             for level2 in d['subNodes']:
    #                 for level3 in level2['subNodes']:
    #                     category_obj = Categories()
    #                     category_obj.id = d['id']
    #                     category_obj.source=level2['source']
    #                     category_obj.sport=level2['sport']
    #                     category_obj.level_1_name=d['name']
    #                     category_obj.level_2_name=level2['name']
    #                     category_obj.level_3_name=level3['name']
    #                     category_obj.league=level3['league']
    #                     category_obj.categoryId=level3['id']
    #                     subNodes_dict[category_obj.league]=category_obj
    #                 self.categories[level2['sport']]=subNodes_dict
    #
    #         # for k in self.categories:
    #         #     for k1 in self.categories[k]:
    #         #         eventId_ls = self.get_eventId_vs_ls(self.categories[k][k1].sport,
    #         #                                self.categories[k][k1].league)

    def _remove_invalid_league(self):
        """去掉无效的league"""
        return_eventId_vs_ls = []
        url = self.testUrl+'/bets-api/upcoming-games?sport=%s&league=%s' \
                               %(self.sport,self.league)
        r = self.session.get(url,headers=self.headers).text

    def _get_eventId_vs_ls(self,sport,league):
        """获取eventId  返回[[eventId,vs]]"""
        return_eventId_vs_ls = []
        url = api_m.upcoming_games%(sport,league)
        if sport == w_v.sport_esports:
            url = api_m.upcoming_games_old%(sport,league)
        # r = self.session.get(url,headers=self.headers).text
        r = self.ev_obj.public_send_request(url).text
        try:

            r_ls = json.loads(r,encoding='utf8')
            c = self._get_categoryId_byleague(sport,league)
            if c != None:
                # if len(r_ls)>0:
                #     print(c.get_levels_name(),league)
                for l in r_ls:
                    temp = []
                    temp.append(l['id'])
                    temp.append(l['vs'])
                    # print('\t',temp)
                    return_eventId_vs_ls.append(temp)
            # print('eventId:',json.dumps(return_eventId_vs_ls,indent=4,ensure_ascii=False))
            return return_eventId_vs_ls
        except:
            return ''

    def _get_event_info_ls (self,sport,league):
        """获取eventId  返回[EventInfo]"""
        return_eventinfo_ls = []
        url = api_m.upcoming_games%(sport,league)
        if sport == w_v.sport_esports:
            url = api_m.upcoming_games_old%(sport,league)
        # r = self.session.get(url,headers=self.headers).text
        r = self.ev_obj.public_send_request(url).text
        try:

            r_ls = json.loads(r,encoding='utf8')
            c = self._get_categoryId_byleague(sport,league)
            if c != None:
                for l in r_ls:
                    event_obj = EventInfo()
                    event_obj.id = l['id']
                    event_obj.vs = l['vs']
                    event_obj.home_id = l['home']['id']
                    event_obj.away_id = l['away']['id']
                    event_obj.start_time = l['time']


                    return_eventinfo_ls.append(event_obj)
            # print('eventId:',json.dumps(return_eventinfo_ls,indent=4,ensure_ascii=False))
            return return_eventinfo_ls
        except:
            return ''

    def _get_templates_response(self,eventId,categoryId,sport,league,source):
        url = api_m.templates%(eventId,categoryId,sport,league,source)
        r = self.ev_obj.public_send_request(url).text
        template_dict = json.loads(r,encoding='utf8')
        if len(template_dict['plays'])>0:
            return r
        else:
            #保存 eventId（目的 下次创建数据时过滤此eventid）
            self._save_invalid_eventId_or_league(sport,eventId)
            return None

    def _create_create_third_game_parmas(self,template_response,noneCenralCurrency_ls=['ETC','ETH']
                ,event_info_obj:EventInfo=None):
        """创建第三方标题的请求参数
        template_response 为 templates请求的响应数据
        """
        game_template = w_v.game_template_file
        templates_dict = json.loads(template_response)
        game_template_dict = json.load(open(game_template,'r',encoding='utf-8'))
        for noneCenralCurrency in noneCenralCurrency_ls:
            game_template_dict['playInfoDTOS'][0]['optionInfoList'][0].setdefault('noneCentralCurrencyOptionDTOEnumMap', {})
            game_template_dict['playInfoDTOS'][0].setdefault('noneCentralCurrencyPlayInfoDTOEnumMap', {})
            game_template_dict['playInfoDTOS'][0]['optionInfoList'][0]['noneCentralCurrencyOptionDTOEnumMap']\
                [noneCenralCurrency]={'betCap':'400','shrink':10000}
            game_template_dict['playInfoDTOS'][0]['noneCentralCurrencyPlayInfoDTOEnumMap']\
                [noneCenralCurrency]={'betCap':'400'}

        game_template_dict['categoryId'] = templates_dict['categoryId']
        game_template_dict['gameTitle'] = templates_dict['gameTitle']
        game_template_dict['source'] = templates_dict['source']
        game_template_dict['outerEventId'] = templates_dict['outerEventId']
        try:
            game_template_dict.setdefault('homeId',event_info_obj.home_id)
            game_template_dict.setdefault('awayId',event_info_obj.away_id)
            game_template_dict.setdefault('startTime',event_info_obj.start_time)
        except:
            pass
        playInfoDTO_template = copy.deepcopy(game_template_dict['playInfoDTOS'][0])
        game_template_dict['playInfoDTOS'].clear()
        for out_play in templates_dict['plays']:
            for play in out_play['plays']:
                game_play = copy.deepcopy(playInfoDTO_template)
                shrink = play['commission']
                game_play['playName']=play['name']
                # print('玩法名称',game_play['playName']['zh'])
                # if game_play['playName']['zh']=='附加让分盘':
                #     print('调试')
                game_play['playDescription']=play['description']
                game_play['playTemplateId']=play['playTemplateId']
                game_play['market']=play['market']
                game_play['round']=play['round']
                game_play['handicap']=play['handicap']
                game_play['awardType']=play['awardType']
                game_play['resultType']=play['resultType']
                game_play_temp = copy.deepcopy(game_play['optionInfoList'][0])
                game_play['optionInfoList'].clear()
                for option in play['optionInfoList']:
                    temp = copy.deepcopy(game_play_temp)
                    temp['index']=option['index']
                    temp['tag']=option['tag']
                    temp['optionName']=option['optionName']
                    # print('\t选项名称',temp['optionName']['zh'])
                    # print('additionalTag',option['additionalTag'])
                    temp['primary']=option['primary']
                    temp['originalOdds']=option['odds']
                    if option['additionalTag'] != None:
                         temp['additionalTag']=option['additionalTag']
                    if shrink != None:
                        shrink = str(shrink)
                    else:
                        shrink = 'null'
                    temp_str = json.dumps(temp['centralCurrencyOptionDTOEnumMap']).replace('10000',shrink)
                    temp['centralCurrencyOptionDTOEnumMap'] = json.loads(temp_str)
                    try:
                        temp_str = json.dumps(temp['noneCentralCurrencyOptionDTOEnumMap']).replace('10000',shrink)
                        temp['noneCentralCurrencyOptionDTOEnumMap'] = json.loads(temp_str)
                    except:
                        pass

                    game_play['optionInfoList'].append(temp)
                game_template_dict['playInfoDTOS'].append(game_play)
        # print(json.dumps(game_template_dict,indent=4,ensure_ascii=False))
        return json.dumps(game_template_dict,indent=4,ensure_ascii=False)


    def _create_game_request_template(self,bet_cap=9000,shrink=10000):
        """创建创建比赛的请求模板"""
        templates_dict = json.load(open(w_v.game_template_file,encoding='utf-8'))
        currency_ls = self._get_test_ev_website_currency()\
                      +w_v.channel_currency.get([self.ev_obj.testEv],[])
        option_currency_dict = {}
        play_currency_dict = {}
        for currency in currency_ls:
            option_currency_dict[currency] = {'betCap':bet_cap,'shrink':shrink}
            play_currency_dict =  {'betCap':bet_cap}
        templates_dict['playInfoDTOS'][0]['optionInfoList'][0]['centralCurrencyOptionDTOEnumMap']\
            = option_currency_dict
        templates_dict['playInfoDTOS'][0]['centralCurrencyPlayInfoDTOEnumMap']\
            = play_currency_dict

        return templates_dict





    def _get_test_ev_website_currency(self):
        """获取测试环境的主站币种"""
        currency_ls = []
        r = self.ev_obj.public_send_request(api_m.currency_init,headers=self.headers).text
        r_dict = json.loads(r,encoding='utf-8')
        for currency_obj in r_dict['backAmtAndUpperLimitList']:
            currency_ls.append(currency_obj['coinType'])

        return currency_ls




    def _get_categoryId_byleague(self,sport,leagueId):
        """通过league获取categoryId
        sportTypeid：体育类别 例 1 体育 19电竞
        返回：Categories类对象
        """
        self._get_category_info()
        try:
            return self.categories[sport][str(leagueId)]
        except:
            return None

    def _get_valid_eventId_ls(self,sport,eventId_ls,index):
        """获取有效的eventId_ls
        步骤：
        1.传入页面获取的eventId_ls
        2.过滤掉文件中的无效的eventId_ls
        3.返回有效的eventId_ls
        """
        invalid_eventId_ls = self._get_invalid_eventId_or_league_ls(sport)
        for invalid_eventId in invalid_eventId_ls:
            for eventId in eventId_ls:
                if invalid_eventId == eventId[index]:
                    eventId_ls.remove(eventId)
        return eventId_ls

    def _get_invalid_eventId_or_league_ls(self,sport,isLeague=False):
        """根据sport获取无效的eventId_ls"""
        file_path = self.invalid_eventId_file
        if isLeague:
            file_path = self.invalid_league_file

        invalid_eventId_dict = json.load(open(file_path,'r',encoding='utf8'))
        testEv_invalid_eventId_dict = invalid_eventId_dict[self.testEv]
        sport_invalid_eventId_ls = []
        try:
            sport_invalid_eventId_ls=testEv_invalid_eventId_dict[sport]
        except:
            pass

        return sport_invalid_eventId_ls

    def _save_invalid_eventId_or_league(self,sport,eventId_or_league,isLeague=False):
        """保存无效的eventId"""
        if self.testEv == w_v.pre:
            file_path = self.invalid_eventId_file
            if isLeague :
                file_path = self.invalid_league_file

            invalid_eventId_dict = json.load(open(file_path,'r',encoding='utf8'))
            testEv_invalid_eventId_dict = invalid_eventId_dict.get(self.testEv)
            if testEv_invalid_eventId_dict == None:
                invalid_eventId_dict[self.testEv] = {}
                testEv_invalid_eventId_dict = {}
                testEv_invalid_eventId_dict[sport] = []

            sport_invalid_eventId_ls = self._get_invalid_eventId_or_league_ls(sport)
            if len(sport_invalid_eventId_ls) > 50:
                sport_invalid_eventId_ls.clear()
            sport_invalid_eventId_ls.append(eventId_or_league)
            testEv_invalid_eventId_dict[sport]=list(set(sport_invalid_eventId_ls))#去重
            fp = open(file_path,'w',encoding='utf8')
            json.dump(invalid_eventId_dict,fp,indent=4)
            fp.close()

    def _save_or_read_eventId(self,eventId,is_read=True):
        """保存或者读取 eventId"""
        file_path = p_v.event_id_file
        eventId_dict = json.load(open(file_path,'r',encoding='utf8'))

        if is_read:
            if eventId_dict.get(str(eventId)) == None:
                return False
            return True
        else:
            eventId_dict[str(eventId)]=eventId
            json.dump(eventId_dict,open(file_path,'w',encoding='utf8'),indent=4)

    def _get_invalid_eventId_or_league_ls(self,sport,isLeague=False):
        """根据sport获取无效的eventId_ls"""
        file_path = self.invalid_eventId_file
        if isLeague:
            file_path = self.invalid_league_file
        sport_invalid_eventId_ls = []

        try:
            invalid_eventId_dict = json.load(open(file_path,'r',encoding='utf8'))
            testEv_invalid_eventId_dict = invalid_eventId_dict[self.testEv]
            sport_invalid_eventId_ls=testEv_invalid_eventId_dict[sport]
        except:
            pass

        return sport_invalid_eventId_ls

    def _is_need_handicap(self,templates_res,case_data_dict):
        """检查比赛对局是否是需要的比赛(正确比分  让分盘口 大小盘口是否包含传入数据)"""
        handicap_dict = {}
        try:
            handicap_dict['correct_score'] = case_data_dict.correct_score
            handicap_dict['alternative_asian_handicap'] = case_data_dict.alternative_asian_handicap
            handicap_dict['alternative_goal_line'] = case_data_dict.alternative_goal_line
        except:
            return True
        templates_obj = dict_to_obj(json.loads(templates_res,encoding='utf-8'))
        plays = templates_obj.plays[0].plays

        act_play_dict = {}
        for play in plays:
            act_play_dict[play.market] = play

        for k,v in handicap_dict.items():
            play = act_play_dict.get(k)
            if  play == None:
                return False
            else:
                # print(k,v,play.market)
                if v != '':
                    arr = v.split('&')
                    tag = arr[0]
                    handicap = arr[1].replace(' ','')
                    find = False
                    for option in play.optionInfoList:
                        # print(tag,handicap,option.tag,option.additionalTag)
                        if tag==option.tag and handicap==option.additionalTag.replace(' ',''):
                            find = True
                            break
                    if find == False:
                        return False
                else:
                    continue
        return True

    def _check_game_is_exist(self,eventId_vs:EventInfo,sport=None):
        """检查game是否存在"""
        event_id = False
        gameId = ''
        if self.testEv == w_v.pre:
            event_id_ls = self._get_invalid_eventId_or_league_ls(sport)
            if str(eventId_vs.id) in str(event_id_ls):
                event_id = True
            else:
                self._save_invalid_eventId_or_league(sport,eventId_vs.id)
        else:
            gameId = self.db.get_gameId(eventId_vs.id)
            if gameId != None:
                event_id = True
            else:
                event_id = False
        if event_id:
            logger.info('比赛已经存在(gameId=%s)：%s'%(gameId,eventId_vs.info()))
        return event_id





class GameLoginAndRegister():
    """登录 注册"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

    @check_step_is_success('登录')
    def login(self,name='shenjun',password='123456',isCrm=True):
        self.headers['Authorization']='Basic YnJvd3Nlcjo='
        url=self.testUrl+'/uaa/oauth/token'
        param = 'username=%s&password=%s&scope=ui&grant_type=password'%(name,password)
        # r = self.session.post(url=url,params=param,headers=self.headers)
        r = self.ev_obj.public_send_request(api_m.login,headers=self.headers,params=param)
        # print('登录后响应数据',r.text)

        if 'error' in r.text:
            return {'text':r.text,'success':False,p_v.is_go_on:False}
        d=json.loads(r.text)
        self.headers['Authorization']='Bearer '+d['access_token']
        self.headers['Content-Type']='application/json;charset=UTF-8'
        # return self.headers;

    def register(self,param_dict):
        """注册用户"""
        name=param_dict['name']
        password=param_dict['password']
        getCoinPwd=param_dict['getCoinPwd']
        print(name,password,getCoinPwd)
        invitationCode=param_dict['invitationCode']
        campaign=param_dict['campaign']


        headers = {'Authorization':'null','Content-Type':'application/json','Origin':self.Origin}
        url=self.testUrl+'/flow/register'
        # r = self.session.get(url,headers=headers).text
        r = self.ev_obj.public_send_request(api_m.register_flow,headers=headers).text
        r = json.loads(r)
        headers['X-Flow-ID']=r['flowId']
        #必须要有此步骤 否则会失败
        # url=self.testUrl+'/vcode/register'
        # r = self.session.options(url,headers=headers)
        r = self.ev_obj.public_send_request(api_m.register_vcode_options,headers=headers)

        #获取验证码
        param='{"receiver":"%s"}'%name
        # r = self.session.post(url=url,data=param,headers=headers)
        r = self.ev_obj.public_send_request(api_m.register_vcode_post,param,headers=headers)

        #提交注册信息
        param = '{"campaign":"%s","invitationCode":"%s","marketingChannel":"",' \
                '"vcode":"123456","email":"%s","password":"%s"}'%(campaign,invitationCode,name,password)
        # url=self.testUrl+'/register'
        # r = self.session.post(url=url,data=param,headers=headers)
        r = self.ev_obj.public_send_request(api_m.register,param,headers=headers)

        result = r.text
        print(name,'注册后响应数据：',r.text)
        #设置提币密码
        self.login(name,password)
        # url=self.testUrl+'/profile/asset-password'
        param='{"assetPassword":"%s"}'%getCoinPwd
        # r = self.session.post(url=url,data=param,headers=self.headers)
        r = self.ev_obj.public_send_request(api_m.asset_password,param)
        print('设置提币后的响应数据：',r.text)
        self.get_ETH_address()

        if 'VCODE_NOT_FOUND' in result:
            return False
        return True


    def get_ETH_address(self):
        # url=self.testUrl+'/profile/request-address'
        # r = self.session.post(url=url,data='{"currency":"ETH"}',headers=self.headers)
        r = self.ev_obj.public_send_request(api_m.request_address,'{"currency":"ETH"}')
        print('获取ETH地址响应数据：',r.text)


class Award():
    """开奖"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)
        self.user_acct_balance_dict = {} #key=userId,value=UserAcctBalanceInfo

    @check_step_is_success('开奖前 读取每个投注用户的资产信息')
    def set_berfore_award_users_acct_balance(self,gameId):
        """设置每个投注用户的开奖前的资产信息"""
        ls = self.ev_obj.db.get_currency_play_info(gameId=gameId)
        users = self.ev_obj.db.get_betting_info_obj_ls(ls,is_get_users=True)

        for user in users:
            #开奖前 获取用户的资产信息
            user_acct = UserAcctBalanceInfo()
            user_acct.set_acct_balance(self.ev_obj.db.get_user_acct_balance_dict(user))
            self.user_acct_balance_dict[user]=user_acct

    @check_step_is_success('开奖后 读取每个投注用户的资产信息')
    def set_after_award_users_acct_balance(self,gameId):
        """设置每个投注用户的开奖后的资产信息"""

        for user,user_acct in self.user_acct_balance_dict.items():
            # user_acct = UserAcctBalanceInfo()
            user_acct.set_acct_balance(self.ev_obj.db.get_user_acct_balance_dict(user),
                                       is_old_acct=False)
            self.user_acct_balance_dict[user]=user_acct


    @check_step_is_success('计算投注用户的获奖金额')
    def set_user_award_amount(self,gameId,option_result_dict):
        """设置用户的获奖金额
        option_result_dict：gameId的每个选项的比赛结果
        """
        currency_play_ls = self.ev_obj.db.get_currency_play_info(gameId=gameId)
        for user,user_acct in self.user_acct_balance_dict.items():
            betting_obj_ls = self.ev_obj.db.get_betting_info_obj_ls(currency_play_ids=currency_play_ls,user_id=user)
            # user_acct = UserAcctBalanceInfo()
            user_acct.set_betting_info(betting_obj_ls,option_result_dict)


    def print_users_acct_balance_info(self):
        """打印用户的资产信息"""
        for user,user_acct in self.user_acct_balance_dict.items():
            # user_acct = UserAcctBalanceInfo()
            print(user,'开奖前的资产信息：\n')
            for k,v in user_acct.old_acct_balance_dict.items():
                # v = AcctBalance()
                print(k,v.__dict__)

            print(user,'开奖后的资产信息：\n')
            for k,v in user_acct.after_award_acct_balance_dict.items():
                # v = AcctBalance()
                print(k,v.__dict__)

            print(user,'中奖金额：\n')
            for k,v in user_acct.betting_dict.items():
                # v = BettingInfo()
                print(k,v.amount,v.return_amount)



    @check_step_is_success('检查用户的冻结金额 可用金额是否正确')
    def check_users_cash(self):
        """检查用户的冻结金额 可用金额是否正确"""
        result_str = ''
        for userId,acctBalanceInfo_obj in self.user_acct_balance_dict.items():
            # acctBalanceInfo_obj = UserAcctBalanceInfo()
            #获取开奖后的用户资产信息
            acctBalanceInfo_obj.set_acct_balance(self.ev_obj.db.get_user_acct_balance_dict(userId)
                ,is_old_acct=False)
            result = acctBalanceInfo_obj.check_frozen_cash()
            result += acctBalanceInfo_obj.check_free_cash()
            if result != '':
                result_str +='用户(%s)资产信息不正确：\n'%userId+result
        # print('断言结果:\n',result_str)

        return p_m.get_public_response(result_str,other_text='')

class NewCreateGameInfo():
    """创建标题类"""

    def __init__(self,ev_obj):
        self.ev_obj = ev_obj
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)
        # self.asian_handicap_dict = {} #key = market_additional_tal 让分
        # self.under_over_dict = {} #key = market_additional_tal 大小球
        self.handicap_dict = {} #key = market_additional_tal val = [OptionsOddsInfo]
        self.play_shrink_dict = {} #key=play_id val = {'quota':'','shrink':''}
        OptionsOddsInfo

    def get_plays_handicap_odds(self,gameId,not_shrink_odds=0):
        """获取多盘口的最终赔率"""
        plays_handicap_ls = self.ev_obj.db.public_query_info((w_sql.plays_handicap%gameId).replace('|','%'))

        for handicap_info in plays_handicap_ls:
            play_id = handicap_info[1]
            play_shrink_ls = self.ev_obj.db.public_query_info(w_sql.play_shrink%play_id)
            for play_shrink in play_shrink_ls:
                option_odds_obj = OptionsOddsInfo()
                quota = float(play_shrink[1])
                shrink = truncate(float(play_shrink[2]),4)
                option_odds_obj.shrink = shrink
                option_odds_obj.central = str(play_shrink[3]).replace("'",'').replace("b\\x0",'')


                option_odds_obj.market = handicap_info[0]
                option_odds_obj.play_id = play_id
                option_odds_obj.original_odds = float(handicap_info[2])
                option_odds_obj.additional_tag = handicap_info[3]
                option_odds_obj.tag = handicap_info[4]
                option_odds_obj.option_id = handicap_info[5]
                key = option_odds_obj.market+'_'+str(option_odds_obj.additional_tag)

                self.play_shrink_dict.setdefault(option_odds_obj.play_id,{'quota':quota,'shrink':shrink})
                if 'ASIAN_HANDICAP' in option_odds_obj.market:
                    if option_odds_obj.tag == 'awayOd':
                        if '+' in option_odds_obj.additional_tag:
                            option_odds_obj.additional_tag = option_odds_obj.additional_tag.replace('+','-')
                        elif '-' in option_odds_obj.additional_tag:
                            option_odds_obj.additional_tag = option_odds_obj.additional_tag.replace('-','+')
                    key = option_odds_obj.market+'_'+str(option_odds_obj.additional_tag)
                if self.handicap_dict.get(key):
                    temp_value_ls = self.handicap_dict.get(key)
                    temp_value_ls.append(option_odds_obj)
                else:
                    self.handicap_dict.setdefault(key,[option_odds_obj])


        for k,v in self.handicap_dict.items():
            print('\n',k,':')
            if len(v)==2:
                R = truncate(1/(truncate(1/v[0].original_odds,4)+truncate(1/v[1].original_odds,4)),4)
                for o in v:
                    # o = OptionsOddsInfo()
                    o.handicap = k
                    o.R = R
                    o.N = truncate(R/o.original_odds,4)
                    shrink = self.play_shrink_dict[o.play_id]['shrink']
                    o.shrink = shrink
                    o.P = truncate((1-shrink)/o.N,2)
                    if o.original_odds <= not_shrink_odds:
                        o.P = o.original_odds
                    o.check_final_odds(self.ev_obj.db,v[0],v[1])
                    # print('\t',o.option_info())

            else:
                print('不成对的盘口',k,' ',v[0].print(),len(v))

        print('end')






if __name__ == '__main__':
    print('test')



