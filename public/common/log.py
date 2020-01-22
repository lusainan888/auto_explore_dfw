# -*- coding: utf-8 -*-

import logging
import time
import os
from coingame.config.globalparam import get_logfile_path


class Log:
    def __init__(self,log_path=None):
        if log_path != None:        #log_path 传参
            self.log_path = log_path
            # print("1:",self.log_path)
        else:
            self.log_path = get_logfile_path()    #log_path 没有传参，默认获取当前目录
            # print("2:",self.log_path)
        self.logname = os.path.join(self.log_path, '{0}.log'.format(time.strftime('%Y-%m-%d')))
        # print("3:",self.logname)

    def __printconsole(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.logname,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    # 日志分级之—debug
    def debug(self,message):
        self.__printconsole('debug', message)

    def info(self,message):
        self.__printconsole('info', message)
        pass

    def warning(self,message):
        self.__printconsole('warning', message)

    def error(self,message):
        self.__printconsole('error', message)


if __name__ == '__main__':
    o=Log()
    o.info(message='first log')
    o.error(message='is error')
    pass
