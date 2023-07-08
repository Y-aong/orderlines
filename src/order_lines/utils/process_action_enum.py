# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_action_enum.py
# Time       ：2023/1/11 21:20
# Author     ：Y-aong
# version    ：python 3.7
# Description：流程和任务状态
"""
import enum


class ProcessStatus(enum.Enum):
    green = 'SUCCESS'
    red = 'FAILURE'
    yellow = 'STOP'
    grey = 'PENDING'
    blue = "RUNNING"


class StatusEnum(enum.Enum):
    grey = 'PENDING'
    blue = 'RUNNING'
    red = 'FAILURE'
    green = 'SUCCESS'
    pink = 'SKIP'
    yellow = 'STOP'
    orange = 'RETRY'
