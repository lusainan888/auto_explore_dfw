#coding=utf-8
from coingame.beans import myunittest
from public.common.util import logger
from coingame.beans import public_values as  p_v
#封装了个check_step_is_success 装饰器
def check_step_is_success(message):
    def fun001(func):
        """检查运行步骤是否成功"""
        def wrapper(self,*args,**kwargs):
            logger.info('开始运行：%s'%(message ))
            res = func(self,*args,**kwargs)
            if res != None and isinstance(res,dict):
                if res['success'] == False:
                    myunittest.CASE_RESULT_TEXT += '\n(操作步骤：%s )失败原因：\n\t%s'\
                                                  %(message,res['text'])
                    #操作失败
                    logger.info('操作失败 原因：%s'%res['text'])

                    if res.get(p_v.is_go_on,False) == False:
                        raise Exception(self.__class__.__name__+'.'+func.__name__)
                    elif res.get(p_v.is_go_on)==None:
                        raise Exception(self.__class__.__name__+'.'+func.__name__)
                else:
                    #操作成功
                    return res
            return res

        return wrapper
    return fun001



if __name__ == '__main__':
    print("test1")
    check_step_is_success("用户投注")
    pass

