# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : check_process_node.py
# Time       ：2023/8/17 23:09
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    检查流程节点是否合法
    check task node is available
"""
from typing import List


class CheckProcessNode:

    def __init__(self, process_info: dict, task_nodes: List[dict], variable: List[dict]):
        self.process_info = process_info
        self.task_nodes = task_nodes
        self.variable = variable

    def check_task_nodes(self):
        """检查任务节点"""
        pass

    def check_variable(self):
        """检查任务变量"""

    def check_process_info(self):
        """检查流程信息"""
        pass

    def check_is_dry(self):
        """检查是否可以dry run"""
        pass
