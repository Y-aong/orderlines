# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : logger.py
# Time       ：2023/1/27 20:19
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    日志文件配置
    logger config
"""
import os
import sys
import logging
import platform
from time import strftime

from conf.config import LoggerConfig

if platform.system().lower() == 'windows':
    appdata_path = os.getenv('APPDATA')
    PATH = os.path.join(appdata_path, 'orderlines_logs')

elif platform.system().lower() == 'linux':
    PATH = os.path.join(LoggerConfig.logger_path, 'orderlines_logs')

FMT = LoggerConfig.FMT
DATE_FMT = LoggerConfig.DATE_FMT


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=FMT, datefmt=DATE_FMT)
        self.log_filename = os.path.join(PATH, f'{strftime("%Y-%m-%d")}.log')
        if not os.path.exists(os.path.abspath(PATH)):
            os.makedirs(PATH)
        self.logger.addHandler(self.get_file_handler(self.log_filename))
        self.logger.addHandler(self.get_console_handler())
        # 设置日志的默认级别,Set the default log level
        self.logger.setLevel(logging.INFO)

    # 输出到文件handler的函数定义
    def get_file_handler(self, filename):
        file_handler = logging.FileHandler(filename, encoding="utf-8")
        file_handler.setFormatter(self.formatter)
        return file_handler

    # 输出到控制台handler的函数定义,Output a function definition to the console handler
    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


logger = Logger().logger
