# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : BaseTask.py
# Time       ：2023/1/15 16:49
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务模型基类
    base task model
"""
from pydantic import BaseModel

from orderlines.utils.process_action_enum import TaskStatus


class BaseTask:

    def __init__(self):
        self.success = TaskStatus.green.value
        self.error = TaskStatus.red.value

    def on_success(self, result: dict, task_name: str):
        """
        自定义你的处理返回值方法
        You can customize your method of handling return values here
        @param result: task result
        @param task_name: task name
        @return:
        """
        pass

    def on_failure(self, error: str, task_name: str):
        """
        自定义你的处理失败信息方法
        Customize your handling of failure messages
        @param error:error info
        @param task_name:task name
        @return:
        """
        pass

    def on_receive(self, param: BaseModel, task_name: str):
        """
        自定义你的处理任务参数方法
        Customize your processing task parameter methods
        @param param: task param
        @param task_name: task name
        @return:
        """
        pass
