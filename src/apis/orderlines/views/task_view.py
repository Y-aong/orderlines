# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_view.py
# Time       ：2023/3/12 10:32
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务视图
    task view
"""
from apis.orderlines.models.task import Task
from apis.orderlines.schema.task_schema import TaskSchema
from public.base_view import BaseView


class TaskView(BaseView):
    url = '/task'

    def __init__(self):
        super(TaskView, self).__init__()
        self.table_orm = Task
        self.table_schema = TaskSchema
