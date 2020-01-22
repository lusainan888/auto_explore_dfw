#coding=utf-8
from coingame.beans import public_values as  p_v

def get_public_response(response,other_text='',is_go_on=False,run_success_text=''):
    """获取响应数据结构"""
    r = '响应数据：%s\n'%(response)
    if other_text != '':
        r += '其它信息：%s'%(other_text)
    request_result = {'text':r,'success':True,p_v.is_go_on:is_go_on}
    if run_success_text == '':
        if len(response)>1:
            request_result['success'] = False
    else:
        if run_success_text not in response:
            request_result['success'] = False
    return request_result


