#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang
import logging
import os
import threading
import time


class Logger:
    def __init__(self):

        #创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def creatLog(self,logname):

        #创建一个handler，用于写入日志文件
        self.local_path = os.getcwd()
        self.log_path = '%s\\%s' % (self.local_path, "logs\\")
        if not os.path.exists(self.log_path):
            os.mkdir('%s\\%s' % (self.local_path, "logs\\"))
        log_path_suffix = time.strftime('%Y-%m-%d-%H-%M-%S')
        logpath = self.log_path + logname +log_path_suffix + '.log'
        # logname = log_path + 'log.log' #指定输出的日志文件名
        if not self.logger.handlers:

            fh = logging.FileHandler(logpath,encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
            fh.setLevel(logging.INFO)

            #创建一个handler，用于将日志输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
        return logpath

    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger
    #
    # def get_log(self):
    #     thread = threading.Thread(target=self.get_log1)
    #     thread.setDaemon(True)
    #     thread.start()
