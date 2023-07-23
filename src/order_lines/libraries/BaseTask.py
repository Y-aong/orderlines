# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : BaseTask.py
# Time       ：2023/1/15 16:49
# Author     ：Y-aong
# version    ：python 3.7
# Description：base task 这里想做任务的动态注册
"""

from order_lines.utils.process_action_enum import StatusEnum


class BaseTask:

    def __init__(self):
        self.success = StatusEnum.green.value
        self.error = StatusEnum.red.value
