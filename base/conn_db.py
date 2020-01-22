# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import psycopg2           #连接postgres数据库

class MypostgresqlUtil():
    def __init__(self,user='postgres',pwd='postgres',
                 host='172.17.3.187',port=5432,db='fabricexplorer'):
        try:
            self.conn = psycopg2.connect(host=host, user=user, password=pwd, port=port, database=db)
            # print('Connect Database Pass!')
        except:
             raise ConnectionError('Connect Database Failed!!!')
        self.cursor = self.conn.cursor()     # 使用 cursor() 方法创建一个游标对象 curs

    def selectInfo(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            #首先fetchone()函数它的返回值是单个的元组,也就是一行记录,如果没有结果,那就会返回null
            #其次是fetchall()函数,它的返回值是多个元组,即返回多个行记录,如果没有结果,返回的是()
            # self.conn.commit()
            print(result[0][0])
            return result
        except:
           # 发生错误时回滚
           print("query error")
if __name__ == '__main__':
    q=MypostgresqlUtil()
    q.selectInfo("select mspid from peer where peer_type='PEER'")
    pass
