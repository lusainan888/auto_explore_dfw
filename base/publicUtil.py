# -*- coding: utf-8 -*-
# __author__ = 'lusn'


import configparser #是用来读取配置文件的包(文件格式包括 ini,.conf)
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
        if data[:3] == codecs.BOM_UTF8:  #判断是否为待BOM文件
            data = data[3:]
            files = codecs.open(configpath, "wb")
            files.write(data)
            files.close()
        fd.close()

        self.cf = configparser.ConfigParser()    #ConfigParser 是用来读取配置文件的包。配置文件的格式如下：中括号“[ ]”内包含的为section。section 下面为类似于key-value 的配置内容。
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

if __name__ == '__main__':
    config_file_path="D:\\explore_dfw\\config"
    o=ReadConfig(os.path.join(config_file_path,'config.ini'))  #读取config.ini
    url=o.getValue('testDomain','testDomain')   #读取config.ini的key=[testDomain]的testDomain值
    print(url)
