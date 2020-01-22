#coding=utf-8

login='/uaa/oauth/token,post'

#以下是注册需要的相关接口
register_flow = '/flow/register,get'
register_vcode_options = '/vcode/register,options'
register_vcode_post = '/vcode/register,post'
register='/register,post' #注册
asset_password = '/profile/asset-password,post' #设置提币密码请求
request_address = '/profile/request-address,post' #获取ETH地址请求


#创建栏目请求
categories = '/forecasts/categories,get'
upcoming_games_old = '/bets-api/upcoming-games?sport=%s&league=%s,get'
upcoming_games = '/lsports-api/upcoming-games?sport=%s&league=%s,get'
templates = '/games/templates?eventId=%s&categoryId=%s&sport=%s&league=%s&source=%s,get'
games = '/games/,post'
get_game_info = '/games/admin/%s,get' #获取game信息

#预测发布
submit_review = '/games/submit-review/,put' #提交部署
pending_deployment_review = '/games/plays/pending-deployment-review/,put' #通过审核
deployment_review = '/games/ACCEPT/deployment-review/,put' #部署
publish_review = '/games/%s/plays/publish-review/,put' #发布
dicard_path = '/games/%s/plays/discard,put' #废弃

#预测管理
close = '/games/plays/close,put' #封盘
revoke = '/games/plays/revoke,put' #撤盘
accept = '/games/plays/review/ACCEPT,put' #审核通过
pending_review = '/games/%s/pending-review,get' #获取 管理员待审核 请求参数
set_score = '/games/result,post' #封盘--设置比分
award = '/games/plays/award,put' #开奖
modify_shrink = '/games/plays/modify-shrink,put' #修改抽水
modify_odds = '/games/plays/modify-odds,put' #修改赔率
modify_award_option = '/games/plays/options/modify-award-option,put' #修改获胜选项
in_prediction_games = '/games/status/IN_PREDICTION?useApi=%s&pageNum=1,get' #获取预测中的gameids
close_games = '/games/status/CLOSED?useApi=%s&pageNum=1,get' #获取封盘中的gameids
fetch_game_amount = '/forecasts/award/fetchGameAmount,post' #获取盈亏

#结算管理
save_win_option_check = '/order/game/crm/action/saveWinOptionCheck,post' #修改获胜选项
save_score_check = 'order/game/crm/action/saveScoreCheck,post' #修改比分
commit_result = '/order/game/crm/action/commitResult,post' #提交初验
calc_game = '/order/game/crm/action/calcGame,post' #提交初验
calc_award = '/order/game/crm/action/award,post' #待开奖直接开奖

#website(主站)
betting = '/forecasts/bet/betting,post' #投注


#CRM
add_or_edit = '/participant/addOrEdit,put' #增加或修改队伍基础数据库
dirtree_image_upload = '/imageUpload/dirtree,post' #上传目录树图片
create_categories = '/forecasts/categories,post' #创建目录树
currency_init = '/refer/setting/init,get' #推广员设置

