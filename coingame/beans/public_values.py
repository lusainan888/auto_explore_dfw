#coding=utf-8
from coingame.config.globalparam import get_project_path

#测试环境
pre = 'pre'
#渠道币种
channel_currency = {'abtest':['BKBT','VET','LBCN','IDA','CT','DCCB','ETC'],
                    'testing':['BKBT','VET','LBCN','IDA','CT','DCCB','ETC']}


ENCODING = 'utf-8'

PENDING_SUBMISSION = 'PENDING_SUBMISSION' #待提交
PENDING_REVIEW = 'PENDING_REVIEW' #待审核
PENDING_DEPLOYMENT = 'PENDING_DEPLOYMENT' #待部署
PENDING_RELEASE = 'PENDING_RELEASE' #待发布
IN_PREDICTION = 'IN_PREDICTION' #预测中
CLOSED = 'CLOSED' #已封盘
CANCELED = 'CANCELED' #已撤销
AWARDED = 'AWARDED' #已开奖
AWARDING = 'AWARDING' #开奖中

STEP_submit_review = 'submit_review' #提交审核
STEP_pending_deployment_review = 'pending_deployment_review' #预测发布-待审核
STEP_deployment_review = 'deployment_review' #预测发布-部署
STEP_publish_review = 'publish_review' #预测发布-发布
STEP_close = 'close' #预测管理-封盘
STEP_accept = 'accept' #预测管理-审核通过
STEP_award = 'award' #预测管理-开奖


is_go_on = 'is_go_on'  #是否继续运行下一步

market_1_1 = '1_1'  #胜平负
double_chance = 'double_chance' #双胜彩
correct_score = 'correct_score' #正确比分
both_teams_to_score = 'both_teams_to_score' #两队均得分
alternative_asian_handicap = 'alternative_asian_handicap' #附加让分盘
alternative_goal_line = 'alternative_goal_line' #附加大小盘

####  栏目类型 #####
# Soccer/Basketball/Tennis/ESPORTS
sport_soccer = 'Soccer'  #足球
sport_basktball = 'Basketball' #篮球
sport_tennis = 'Tennis' #网球
sport_baseball = 'Baseball' #棒球
sport_darts = 'Darts' #飞镖
sport_volleyball = 'Volleyball' #排球
sport_snooker = 'Snooker' #斯诺克
sport_esports = 'ESPORTS' #电竞
sport_my_funny = 'my_funny'  #自定义趣味竞猜

#体育类别league_id
sport_league_dict = {sport_soccer:1,sport_basktball:2,sport_baseball:3,sport_tennis:4
        ,sport_volleyball:5,sport_snooker:6,sport_darts:7}


participant_start_index = 100000000000000
participant_start_base_id = 1000
#fixture_id的基础id 根据体育类别计算fixture_id=league*fixture_id（注：fixture_base_id的最大位数为9位数）
fixture_base_id  = 100000000


#文件路径
data_path = get_project_path()+'/coingame/data/coingame'
event_id_file = data_path + '/eventId_dict.txt'
lsports_mq_template_file = get_project_path()+'/coingame/data/mock_data' \
                           '/template/lsports_mq_template.json' #lsports MQ模板

lsports_mock_data_file = get_project_path()+'/coingame/data/mock_data' \
                    '/template/lsports_mock_data.xlsx'

mock_data_config = get_project_path()+'/coingame/data/mock_data' \
                           '/template/mock_data_config.json'

odds_template_file = get_project_path()+'/coingame/data/mock_data' \
                           '/template/odds_template.json'

participant_start_id_file = get_project_path()+'/coingame/data/mock_data' \
                           '/template/participant_start_id.txt'

icon_path = get_project_path()+'/coingame/data/mock_data' \
                           '/icon/'


game_template_file = get_project_path()+'/coingame/data/coingame/interface_template_data/games_template.json'



mq_url='http://172.17.2.103:15672/api/exchanges/%2F/amq.default/publish'


upimage_content_type = 'multipart/form-data; boundary=----WebKitFormBoundaryMrE7uhYsRxtVnCVu'

boundary = '----WebKitFormBoundaryMrE7uhYsRxtVnCVu'

