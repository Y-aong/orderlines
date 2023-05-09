# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : logger.py
# Time       ：2023/1/27 20:19
# Author     ：blue_moon
# version    ：python 3.7
# Description：日志
"""
import os
import sys
import logging
import platform
from time import strftime

from conf.config import LoggerConfig

# 输出日志路径
if platform.system().lower() == 'windows':
    appdata_path = os.getenv('APPDATA')
    PATH = os.path.join(appdata_path, 'order_lines')

elif platform.system().lower() == 'linux':
    PATH = os.path.join(LoggerConfig.linux_logger_path, 'order_lines')

# 设置日志格式#和时间格式
FMT = LoggerConfig.FMT
DATE_FMT = LoggerConfig.DATE_FMT


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=FMT, datefmt=DATE_FMT)
        self.log_filename = f'{PATH}\\{strftime("%Y-%m-%d")}.log'
        if not os.path.exists(os.path.abspath(PATH)):
            os.makedirs(PATH)
        self.logger.addHandler(self.get_file_handler(self.log_filename))
        self.logger.addHandler(self.get_console_handler())
        # 设置日志的默认级别
        self.logger.setLevel(logging.INFO)

    # 输出到文件handler的函数定义
    def get_file_handler(self, filename):
        file_handler = logging.FileHandler(filename, encoding="utf-8")
        file_handler.setFormatter(self.formatter)
        return file_handler

    # 输出到控制台handler的函数定义
    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


logger = Logger().logger
