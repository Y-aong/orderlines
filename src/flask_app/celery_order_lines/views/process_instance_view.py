# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_instance_view.py
# Time       ：2023/3/12 13:20
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app.celery_order_lines.models.order_line_models import ProcessInstanceModel
from flask_app.celery_order_lines.schema.order_lines_schema import ProcessInstanceSchema
from flask_app.public.base_view import BaseView


class ProcessInstanceView(BaseView):
    url = '/process_instance'

    def __init__(self):
        super(ProcessInstanceView, self).__init__()
        self.table_orm = ProcessInstanceModel
        self.table_schema = ProcessInstanceSchema
