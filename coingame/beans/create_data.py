#coding=utf-8
from coingame.beans.readCaseInfo import ReadRunCaseData
from coingame.config.globalparam import get_project_path, get_data_path, get_testEv
from coingame.config.testEnvironmentManager1 import TestEnvironment
from public.common.util import OperatorExcel, del_file, add_sub_date, dict_to_obj
import json
import copy
from coingame.beans import public_values as w_v
import requests
import time
import datetime


def get_awar_handicap(handicap):
    handicap = str(handicap)
    if '+' in handicap:
        return handicap.replace('+','-')
    elif '-' in handicap:
        return handicap.replace('-','+')
    return handicap

class CreateSoccerMockData():
    """创建足球 篮球的mock_data"""


    def __init__(self,mock_file=''):
        self.mock_template_file_path = get_data_path()+'mock_data/template/'
        self.mock_file_path = get_data_path()+'mock_data/'
        self.mock_file = self.mock_template_file_path+'mock_data.xlsx'
        self.mock_data_config = self.mock_template_file_path+'mock_data_config.json'
        self.excel = OperatorExcel(self.mock_file)
        self.testEv = get_testEv()

        self._get_register_users_dict_ls()


    def _get_register_users_dict_ls(self):
        poisql='register_user&isRegister=yes&0'
        self.register_users_dict_ls = self.excel.getData2DictList(poisql)

    def _read_league_start_index(self,league):
        """读取league开始eventId"""
        fp = open(self.mock_data_config,'r',encoding='utf-8')
        cofig_dict = json.load(fp)
        fp.close()
        return cofig_dict[self.testEv]['league_%s'%league]

    def _write_league_start_index(self,league,start_index):
        """读取league开始eventId"""
        fp = open(self.mock_data_config,'r',encoding='utf-8')
        cofig_dict = json.load(fp)
        fp.close()
        cofig_dict[self.testEv]['league_%s'%league] = start_index
        fp = open(self.mock_data_config,'w',encoding='utf-8')
        json.dump(cofig_dict,fp,ensure_ascii=False,indent=4)
        fp.close()


    def create_upcoming_file(self):
        del_file(self.mock_file_path)
        upcoming_template = self.mock_template_file_path+'upcoming_template.json'
        temp_dict = json.load(open(upcoming_template,'r',encoding='utf-8'))

        sql = 'mock_data&isRun=yes&0'
        dict_ls = self.excel.getData2DictList(sql)
        for d in dict_ls:
            temp_dict_copy = copy.deepcopy(temp_dict)
            temp_dict_copy['pager']['total'] = d['create_count']
            old_index = self._read_league_start_index(d['league'])
            start_id = int(d['start_id'])+ old_index
            create_count = int(d['create_count'])
            self._write_league_start_index(d['league'],old_index+create_count)
            start_bet365_id = int(d['start_bet365_id'])+ old_index
            results_dict_old = copy.deepcopy(temp_dict_copy['results'][0])
            temp_dict_copy['results'].clear()
            for i in range(create_count):
                results_dict = copy.deepcopy(results_dict_old)
                results_dict['id'] =start_id + i
                results_dict['sport_id'] =d['sport_id']
                results_dict['league']['name'] =d['name']
                results_dict['home']['name'] = 'AUTO_A_'+str(start_id + i)
                results_dict['away']['name'] = 'AUTO_B_'+str(start_id + i)
                temp_dict_copy['results'].append(results_dict)
                bet365_id = start_bet365_id + i
                self.create_view_data(d['sport_id'],start_id + i,bet365_id)
                self.create_start_sp(bet365_id,start_id + i,d['m_id'])

            text = json.dumps(temp_dict_copy,indent=4,ensure_ascii=False)

            file_name = d['type']+'_'+d['league']+'_upcoming.json'
            old_text_dict = {}
            old_total = 0
            old_text_results = []
            fp = None
            try :
                fp = open(self.mock_file_path+file_name,'r',encoding='utf-8')
                old_text_dict = json.load(fp)
                old_total = old_text_dict['pager']['total']
                old_text_results = old_text_dict['results']
                fp.close()
            except:
                pass

            new_total = temp_dict_copy['pager']['total']
            temp_dict_copy['pager']['total'] = int(old_total) + int(new_total)
            temp_dict_copy['results'] = old_text_results + temp_dict_copy['results']
            fp = open(self.mock_file_path+file_name,'w',encoding='utf-8')
            json.dump(temp_dict_copy,fp
                    ,ensure_ascii=False,indent=4)
            fp.close()

            self.excel.close()


    def create_view_data(self,sportId,eventId,bet365_id):
        view_template = self.mock_template_file_path+'view_template.json'
        temp_dict = json.load(open(view_template,'r',encoding='utf-8'))

        temp_dict['results'][0]['id'] = str(eventId)
        temp_dict['results'][0]['sport_id'] = str(sportId)
        temp_dict['results'][0]['bet365_id'] = str(bet365_id)

        text = json.dumps(temp_dict,indent=4,ensure_ascii=False)
        file_name = '%s_view.json'%eventId
        fp = open(self.mock_file_path+file_name,'w',encoding='utf-8')
        fp.write(text)

    def create_start_sp(self,bet365_id,event_id,m_id):

        view_template = self.mock_template_file_path+'start_sp_template.json'
        temp_dict = json.load(open(view_template,'r',encoding='utf-8'))

        result_dict = temp_dict['results'][0]
        result_dict['FI'] = str(bet365_id)
        result_dict['event_id'] = str(event_id)

        asian_handicap = []
        goal_line = []
        alternative_asian_handicap = []
        alternative_goal_line = []
        correct_score = []

        sql = 'additional_tag&m_id=%s&0'%m_id
        res_dict_ls = self.excel.getData2DictList(sql)

        #设置alternative_asian_handicap相关信息
        i = 0
        for d in res_dict_ls:
            home_opp = str(d['asian_handicap'])
            if home_opp != '':
                away_opp = str(get_awar_handicap(home_opp))
                home_odds = str(d['asian_handicap_home_odds'])
                away_odds = str(d['asian_handicap_away_odds'])
                home_dict = {"opp":home_opp,"odds":home_odds,"header":"Home"}
                away_dict = {"opp":away_opp,"odds":away_odds,"header":"Away"}
                if i == 0:
                    asian_handicap.append(home_dict)
                    asian_handicap.append(away_dict)
                else:
                    alternative_asian_handicap.append(home_dict)
                    alternative_asian_handicap.append(away_dict)
                i +=1

        #设置goal_line相关信息
        i = 0
        for d in res_dict_ls:
            home_opp = str(d['goal_line'])
            if home_opp != '':
                away_opp = str(get_awar_handicap(home_odds))
                over_odds = str(d['goal_line_over_odds'])
                under_odds = str(d['goal_line_under_odds'])
                over_dict = {"goals":home_opp,"odds":over_odds,"header":"Over"}
                under_dict = {"goals":home_opp,"odds":under_odds,"header":"Under"}
                if i == 0:
                    goal_line.append(over_dict)
                    goal_line.append(under_dict)
                else:
                    alternative_goal_line.append(over_dict)
                    alternative_goal_line.append(under_dict)
                i +=1

        #设置correct_score相关信息
        for d in res_dict_ls:
            correct_score_home = d['correct_score_home']
            correct_score_x = d['correct_score_x']
            correct_score_away = d['correct_score_away']
            if correct_score_home != '':
                temp = {"opp":correct_score_home,"odds":d['correct_score_home_odds'],"header":"Home"}
                correct_score.append(temp)
            if correct_score_x != '':
                temp = {"opp":correct_score_x,"odds":d['correct_score_x_odds'],"header":"X"}
                correct_score.append(temp)
            if correct_score_away != '':
                temp = {"opp":correct_score_away,"odds":d['correct_score_away_odds'],"header":"Away"}
                correct_score.append(temp)

        result_dict['asian_lines']['sp']['asian_handicap']=asian_handicap
        result_dict['asian_lines']['sp']['goal_line']=goal_line
        result_dict['asian_lines']['sp']['alternative_asian_handicap']=alternative_asian_handicap
        result_dict['asian_lines']['sp']['alternative_goal_line']=alternative_goal_line
        result_dict['main']['sp']['correct_score']=correct_score

        self.pop_key(result_dict['asian_lines']['sp'],'asian_handicap')
        self.pop_key(result_dict['asian_lines']['sp'],'goal_line')
        self.pop_key(result_dict['asian_lines']['sp'],'alternative_asian_handicap')
        self.pop_key(result_dict['asian_lines']['sp'],'alternative_goal_line')
        self.pop_key(result_dict['main']['sp'],'correct_score')

        text = json.dumps(temp_dict,indent=4,ensure_ascii=False)
        file_name = '%s_start_sp.json'%bet365_id
        fp = open(self.mock_file_path+file_name,'w',encoding='utf-8')
        fp.write(text)

    def pop_key(self,map,key):
        if len(map[key]) == 0:
            map.pop(key)


class CreateLsportsMockData():
    """创建lsports  mock_data"""

    def __init__(self,ev_obj:TestEnvironment):
        self.ev_obj = ev_obj
        self.testEv = self.ev_obj.testEv
        for k,v in ev_obj.__dict__.items():
            setattr(self,k,v)

        self.lsports_template_dict = json.load(open(w_v.lsports_mq_template_file,encoding='utf-8'))
        self.events_ls = self.lsports_template_dict['Body']['Events'][0]
        self.fixture_dict = self.events_ls['Fixture']
        livescore_dict = self.events_ls['Livescore']
        self.markets_dict = self.events_ls['Markets'][0]
        self.events_ls['Fixture'] = None
        self.events_ls['Livescore'] = None
        self.events_ls['Markets'] = None
        self.case  = ReadRunCaseData(other_path=w_v.lsports_mock_data_file)
        self.mock_data_config = w_v.mock_data_config
        self.case_ls = self.case.get_cases()


    def create_match(self):
        """创建比赛对局"""
        for case_obj in self.case_ls:
            case_obj = case_obj[0]
            self.lsports_template_dict['Header']['Type'] = 1

            for i in range(int(case_obj.create_num)):
                fixture_id = self._read_fixture_id_start_index(case_obj.league)
                # fixture_id = 12
                self.events_ls['FixtureId'] = fixture_id
                lsports_match_dict = copy.deepcopy(self.lsports_template_dict) #推送比赛对局消息体
                if case_obj.type == '0':
                    self.fixture_dict['Sport']['Id'] = case_obj.sport_id
                    self.fixture_dict['Sport']['Name'] = case_obj.sport_type
                    self.fixture_dict['StartDate'] = add_sub_date(datetime.datetime.now(),
                                                day=7,date_format='%Y-%m-%dT%H:%M:%S')
                    self.fixture_dict['Participants'][0]['Name']='auto_%s_a'%fixture_id
                    self.fixture_dict['Participants'][1]['Name']='auto_%s_b'%fixture_id
                    self.fixture_dict['Participants'][0]['Id']=self.read_participant_start_id(case_obj.sport_type)
                    self.fixture_dict['Participants'][1]['Id']=self.read_participant_start_id(case_obj.sport_type)
                    self.fixture_dict['Status']=1
                    self.fixture_dict['Sport']['Id']=int(case_obj.sport_id)
                    self.fixture_dict['Location']['Id']=int(case_obj.location_id)
                    self.fixture_dict['League']['Id']=int(case_obj.league)

                    lsports_match_dict['Body']['Events'][0]['Fixture'] = self.fixture_dict
                    self.publish_mq(lsports_match_dict,self.testEv)
                    #需要等待1min（把比赛创建成功后 才能处理玩法赔率）
                    time.sleep(12)

                    self.create_odds_msg(case_obj)
                    print('消息发送完毕')


            print('temp')


    def create_odds_msg(self,case_obj):
        """创建赔率 消息"""
        poisql = 'play_info&pid=%s&0'%case_obj.pid
        plays_ls = self.case.excel.getData2DictList(poisql)
        final_market_ls = []
        for play_dict in plays_ls:
            lsports_msg_body_dict = copy.deepcopy(self.lsports_template_dict) #推送比赛对局消息体
            lsports_msg_body_dict['Header']['Type'] = 3

            play_obj = dict_to_obj(play_dict)
            play_market_dict = copy.deepcopy(self.markets_dict)
            play_market_dict['Id'] = play_obj.market_id
            play_market_dict['Name'] = play_obj.market_name

            odds_template_dict = json.load(open(w_v.odds_template_file,encoding='utf_8'))
            market_odds = odds_template_dict[play_obj.market_name]
            odds_sheet = play_obj.odds_sheet

            if odds_sheet.strip() != '':
                poisql = '%s&odds_id=%s&0'%(odds_sheet,play_obj.odds_id)
                odds_ls = self.case.excel.getData2DictList(poisql)

                if odds_sheet == 'asian':
                    play_market_dict['Providers'][0]['Bets'] = self._create_asian_market(market_odds,odds_ls)
                elif  odds_sheet == 'goal_line':
                    play_market_dict['Providers'][0]['Bets'] = self._create_goal_line_market(market_odds,odds_ls)
                elif  odds_sheet == 'score':
                    play_market_dict['Providers'][0]['Bets'] = self._create_correct_score_market(market_odds,odds_ls)
            else:
                play_market_dict['Providers'][0]['Bets'] = market_odds

            final_market_ls.append(play_market_dict)
        lsports_msg_body_dict['Body']['Events'][0]['Markets'] = final_market_ls
        self.publish_mq(lsports_msg_body_dict,self.testEv)





    def _create_asian_market(self,market_odds,odds_ls):
        final_odds_ls = []
        for odds_dict in odds_ls:
            handicap = float(str(odds_dict['handicap']).replace(' ',''))
            away_handicap = -handicap

            home_odds = copy.deepcopy(market_odds[0])
            home_odds['Name'] = '1'
            home_odds['Price'] = odds_dict['home_odds']
            home_odds['Line'] = '%s (0-0)'%handicap

            away_odds = copy.deepcopy(market_odds[0])
            away_odds['Name'] = '2'
            away_odds['Price'] = odds_dict['away_odds']
            away_odds['Line'] = '%s (0-0)'%away_handicap
            final_odds_ls.append(home_odds)
            final_odds_ls.append(away_odds)
        return final_odds_ls

    def _create_goal_line_market(self,market_odds,odds_ls):
        final_odds_ls = []
        for odds_dict in odds_ls:
            handicap = str(odds_dict['handicap']).replace(' ','')

            home_odds = copy.deepcopy(market_odds[0])
            home_odds['Name'] = 'Over'
            home_odds['Price'] = odds_dict['over_odds']
            home_odds['Line'] = handicap

            away_odds = copy.deepcopy(market_odds[0])
            away_odds['Name'] = 'Under'
            away_odds['Price'] = odds_dict['under_odds']
            away_odds['Line'] = handicap

            final_odds_ls.append(home_odds)
            final_odds_ls.append(away_odds)
        return final_odds_ls

    def _create_correct_score_market(self,market_odds,odds_ls):
        final_odds_ls = []
        for odds_dict in odds_ls:
            home_odds = copy.deepcopy(market_odds[0])
            home_odds['Name'] = odds_dict['score']
            home_odds['Price'] = odds_dict['odds']
            final_odds_ls.append(home_odds)
        return final_odds_ls



    def _publish_match(self,case_obj):
        """推送比赛对局"""


    def _read_fixture_id_start_index(self,league):
        """读取league开始eventId"""
        fp = open(self.mock_data_config,'r',encoding='utf-8')
        cofig_dict = json.load(fp)
        fp.close()
        fixture_id = 1
        final_fixture_id = 0
        try:
            fixture_id = cofig_dict[self.testEv]['league_%s'%league]
        except:
            pass
        self._write_fixture_id_start_index(league,fixture_id+1)

        return   w_v.fixture_base_id*int(league)+fixture_id

    def _write_fixture_id_start_index(self,league,start_index):
        """读取league开始eventId"""
        fp = open(self.mock_data_config,'r',encoding='utf-8')
        cofig_dict = json.load(fp)
        fp.close()
        cofig_dict[self.testEv]['league_%s'%league] = start_index
        fp = open(self.mock_data_config,'w',encoding='utf-8')
        json.dump(cofig_dict,fp,ensure_ascii=False,indent=4)
        fp.close()


    def publish_mq (self,msg,test_ev='testing'):
        """推送MQ"""
        if isinstance(msg,dict):
            msg = json.dumps(msg,ensure_ascii=False)
        print(msg)
        msg = msg.replace('"','\\"')

        session = requests.Session()
        headers={'Authorization':'Basic Z3Vlc3Q6Z3Vlc3Q='}

        params = '{"vhost":"/","name":"amq.default","properties":{"delivery_mode":1,"headers":{}},"routing_key":"lsports_mq_%s","delivery_mode":"1",' \
                 '"payload":"%s","headers":{},' \
                 '"props":{},"payload_encoding":"string"}'% (test_ev,msg)
        cookie={'auth':'Z3Vlc3Q6Z3Vlc3Q%3D'}

        r = session.post(url=w_v.mq_url,headers=headers,data=params,cookies=cookie)

        print('推送消息后响应数据:',r.text)
        # time.sleep(12)



    def read_participant_start_id(self,sport_type):
        """读队伍基础数据id 1-40 循环取用"""
        fp = open(w_v.participant_start_id_file)
        participant_start_id = int(fp.read())
        if participant_start_id > 40:
            self.write_participant_start_id(1)
        else:
            self.write_participant_start_id(participant_start_id+1)
        start_index = w_v.sport_league_dict[sport_type]*w_v.participant_start_index
        return  start_index + participant_start_id+w_v.participant_start_base_id

    def write_participant_start_id(self,index):
        """写队伍基础数据id"""
        fp = open(w_v.participant_start_id_file,'w')
        fp.write(str(index))
        fp.close()


if __name__ == '__main__':
    c = CreateSoccerMockData()
    c.create_upcoming_file()


    pass


