# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_enum.py
# Time       ：2023/1/11 21:20
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程和任务状态
    Process and task status
"""
import enum


class ProcessStatus(enum.Enum):
    green = 'SUCCESS'
    red = 'FAILURE'
    yellow = 'STOP'
    grey = 'PENDING'
    blue = "RUNNING"
    purple = "PAUSED"


class TaskStatus(enum.Enum):
    grey = 'PENDING'
    blue = 'RUNNING'
    red = 'FAILURE'
    green = 'SUCCESS'
    pink = 'SKIP'
    yellow = 'STOP'
    orange = 'RETRY'


class TaskType(enum.Enum):
    common = 'common'
    process_control = 'process_control'
    group = 'group'
    parallel = 'parallel'
    remote = 'remote'
    start = 'start'
    end = 'end'
