# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : BuiltIn.py
# Time       ：2023/2/19 19:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
内建函数包含开始结束任务
Built-in functions contain start and end tasks
"""
from conf.config import OrderLinesConfig
from orderlines.libraries.BaseTask import BaseTask
from orderlines.utils.base_orderlines_type import BasePluginParam


class BuiltIn(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self):
        super(BuiltIn, self).__init__()

    def start(self, base_param: BasePluginParam) -> dict:
        """
        开始节点
        start node
        """
        return {'status': self.success}

    def end(self, base_param: BasePluginParam) -> dict:
        """
        结束节点
        end node
        """
        return {'status': self.success}

    def select(self, base_param: BasePluginParam) -> dict:
        """
        标记节点
        select node
        """
        return {'status': self.success}
