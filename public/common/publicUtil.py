# -*- coding: utf-8 -*-

import configparser #是用来读取配置文件的包
import codecs       #处理任意编码的字符
import pymysql      #连接mysql数据库
import psycopg2           #连接postgres数据库
import math
import os
class ReadConfig:
    """
    专门读取配置文件的，.ini文件格式
    """
    def __init__(self, filename):
        # configpath = os.path.join(prjDir,filename)
        configpath = filename
        # print(configpath)
        fd = open(configpath)
        data = fd.read()
        # remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            files = codecs.open(configpath, "wb")
            files.write(data)
            files.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def getValue(self, env, name):
        """
        [projectConfig]
        project_path=E:/Python-Project/UItestframework
        :param env:[projectConfig]
        :param name:project_path
        :return:E:/Python-Project/UItestframework
        """
        return self.cf.get(env,name)

class MysqlUtil():

    def __init__(self,user='testing',pwd='testing',
                 host='172.17.1.128',port=3306,db='sp_test'):
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, db=db, charset='utf8')
        except:
             raise ConnectionError('Connect Database Failed!!!')
        # self.conn.autocommit(10000)
        self.cursor = self.conn.cursor()     # 使用 cursor() 方法创建一个游标对象 curs

    def selectInfo(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            #首先fetchone()函数它的返回值是单个的元组,也就是一行记录,如果没有结果,那就会返回null
            #其次是fetchall()函数,它的返回值是多个元组,即返回多个行记录,如果没有结果,返回的是()
            # self.conn.commit()
            # print(result[0][0])
            return result
        except:
           # 发生错误时回滚
           print("query error")

    def update(self,sql):
        try:
            result=self.cursor.execute(sql)
            self.conn.commit()
            return result
        except:
            print("update error")
            self.conn.rollback() #update ,insert , delete）未commit 之前 使用rollback 可以恢复数据到修改之前
    def insert(self,sql):
        try:
            result=self.cursor.execute(sql)
            self.conn.commit()
            return result
        except:
            print("insert error")
            self.conn.rollback()

    def delete(self,sql):
        try:
            result=self.cursor.execute(sql)
            self.conn.commit()
            return result
        except:
            print("delete error")
            self.conn.rollback()

    def insertmany1(self, sql, args, batchsize=100):
        loop = math.ceil(len(args) / batchsize)  #向上取整
        args_list = [
            args[i:i + batchsize] for i in range(0, len(args), batchsize)
        ]

        for index in range(loop):
            self.cursor.executemany(sql, args_list[index])
            self.conn.commit()

    def insertmany(self, sql, args):
            reult=self.cursor.executemany(sql, args)
            self.conn.commit()
            return result

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

class MypostgresqlUtil():
    def __init__(self,user='postgres',pwd='postgres',
                 host='172.17.3.196',port=5432,db='fabricexplorer'):
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
            # print(result[0][0])
            return result
        except:
           # 发生错误时回滚
           print("query error")
if __name__ == '__main__':
    # o=ReadConfig("D:\\auto_test_nancy\\12.txt") #???
#
#     #mysql
#     p=MysqlUtil(db='sp_test')
#     # p=MysqlUtil( host='172.17.3.163',db='sp_beta')
#     p.selectInfo('select id from users where email="555@qq.com"')  #查询OK
#     sql='select id from users where email="555@qq.com"'
#     p.selectInfo(sql)
#     #p.selectInfo('select id from users where email="%s"' %("555@qq.com"))  #查询OK
#     #p.update('UPDATE users SET email="555D@qq.com" where id=1640') #修改OK
#     # p.insert("INSERT INTO `acct_balance` (`user_id`,`product_code`,`currency`,`frozen_cash`,`free_cash`,`is_deleted`)"\
#     #         "VALUES('1640','2001','BCH3','0.000000000000000000','0.000000000000000000','0')")#新增OK---1
#     #sql="INSERT INTO `acct_balance` (`user_id`,`product_code`,`currency`,`frozen_cash`,`free_cash`,`is_deleted`)\
# #         VALUES('1640','2001','BCH4','0.000000000000000000','0.000000000000000000','0')"
# #
# #     sql="INSERT INTO `acct_balance` (`user_id`,`product_code`,`currency`,`frozen_cash`,`free_cash`,`is_deleted`) " \
# #         "VALUES(%s,%s,'%s',%s,%s,%s)" %('1640','2001','BCH6','0.000000000000000000','0.000000000000000000','0')
# #     p.insert(sql)#新增OK---2
#
#     #p.delete('delete from acct_balance where user_id=1640 and currency="BCH1";')#删除OK
#     #list=['zhangsan','2013-05-20 20:18:16','admin']
#
#     '''
#     list1=[('1640','2001','BCH11','0.000000000000000000','0.000000000000000000','0'),\
#           ('1640','2001','BCH112','0.000000000000000000','0.000000000000000000','0'),\
#           ('1640','2001','BCH13','0.000000000000000000','0.000000000000000000','0')]
#     #print(type(list1)) #<class 'list'>
#     p.insertmany1("INSERT INTO `acct_balance` (`user_id`,`product_code`,`currency`,`frozen_cash`,`free_cash`,`is_deleted`) VALUES(%s,%s,%s,%s,%s,%s)",list1) #insertmany OK
#     '''
#     p.close()


    #postgresql
    # q=MypostgresqlUtil()
    # q.selectInfo("select mspid from peer where id=19")


    config_file_path="D:\\auto_test_nancy\\coingame\\config"
    o=ReadConfig(os.path.join(config_file_path,'config.ini'))
    url=o.getValue('testDomain','testDomain')
    print(url)



    pass
