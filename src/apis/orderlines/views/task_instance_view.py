# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_instance_view.py
# Time       ：2023/3/12 13:21
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务实例视图
    task instance view
"""
from apis.orderlines.models.task import TaskInstance
from apis.orderlines.schema.task_schema import TaskInstanceSchema
from public.base_view import BaseView


class TaskInstanceView(BaseView):
    url = '/task_instance'

    def __init__(self):
        super(TaskInstanceView, self).__init__()
        self.table_orm = TaskInstance
        self.table_schema = TaskInstanceSchema
