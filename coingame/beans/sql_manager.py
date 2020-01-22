#coding=utf-8


game_plays = 'SELECT play_id,market from fortune_base_play_info where game_id = %s;'

#获取动态赔付转换币种
dynamic_currency = "SELECT currency from fortune_option_odds_gradient where is_effect='00' limit 1"


#获取玩法盘口
additional_tag = "SELECT o.additional_tag,o.* from fortune_base_play_option_info o " \
    "where play_id =%s and tag='%s';"

#获取非中心化赔率变化记录
modify_odds = "SELECT odds from fortune_modify_odds_record " \
    "where currency_play_id in (%s) and end_time is NULL %s;"

#获取option_id
option_ids = "SELECT option_id from fortune_base_play_option_info WHERE play_id=%s"

#获取玩法Id
currency_play_ids = "SELECT id,currency from fortune_currency_play_info WHERE play_id=%s;"

#根据optionId 获取 currency_play_id currency_option_id
currency_play_and_option_ids_by_optionId = """
    SELECT c_p_i.id currency_play_id,c_o_i.id currency_option_id,c_o_i.currency
	from fortune_currency_option_info c_o_i,fortune_base_play_option_info b_p_o,fortune_currency_play_info c_p_i
		WHERE c_o_i.option_id=b_p_o.option_id and c_p_i.play_id=b_p_o.play_id
			and c_p_i.currency=c_o_i.currency and c_o_i.option_id=%s and c_o_i.central=1;
"""


all_bet_amount_by_currency_play_id = "SELECT sum(amount) from fortune_betting_record WHERE currency_play_id=%s;"

#最终赔率
final_odds = "SELECT final_odds from fortune_currency_option_info WHERE id=%s;"


sport_id = "SELECT id from fortune_category where `name` like '%\"{var}\"%' and league is null"

