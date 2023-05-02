# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_view.py
# Time       ：2023/3/12 13:18
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app.order_lines_app.models.order_line_models import ProcessModel
from flask_app.order_lines_app.schema.order_lines_schema import ProcessSchema
from flask_app.public.base_view import BaseView


class ProcessView(BaseView):
    url = '/process'

    def __init__(self):
        super(ProcessView, self).__init__()
        self.table_orm = ProcessModel
        self.table_schema = ProcessSchema
