# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_instance_view.py
# Time       ：2023/3/12 13:21
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app.celery_order_lines.models.order_line_models import TaskInstanceModel
from flask_app.celery_order_lines.schema.order_lines_schema import TaskInstanceSchema
from flask_app.public.base_view import BaseView


class TaskInstanceView(BaseView):
    url = '/task_instance'

    def __init__(self):
        super(TaskInstanceView, self).__init__()
        self.table_orm = TaskInstanceModel
        self.table_schema = TaskInstanceSchema
