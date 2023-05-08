# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_view.py
# Time       ：2023/3/12 10:32
# Author     ：blue_moon
# version    ：python 3.7
# Description：任务的增删改查
"""
from flask_app.celery_order_lines.models.order_line_models import TaskModel
from flask_app.celery_order_lines.schema.order_lines_schema import TaskSchema
from flask_app.public.base_view import BaseView


class TaskView(BaseView):
    url = '/task'

    def __init__(self):
        super(TaskView, self).__init__()
        self.table_orm = TaskModel
        self.table_schema = TaskSchema
