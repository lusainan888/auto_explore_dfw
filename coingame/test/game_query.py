# -*- coding: utf-8 -*-
# __author__ = 'lusn'
#利用mysql查询数据库的实例
from public.common.publicUtil import MysqlUtil
#1、#2、第三方报表收益核对
# print(result[0][0])
def getuser():
    sql='select id from users where email="555@qq.com"'
    queryresult=MysqlUtil.selectInfo(sql)
    return queryresult

if __name__ == '__main__':
    mysql = MysqlUtil(user='testing',pwd='testing',
                 host='172.17.1.128',port=3306,db='sp_test')
    getuser()
