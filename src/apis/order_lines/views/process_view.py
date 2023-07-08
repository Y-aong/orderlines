# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_view.py
# Time       ：2023/3/12 13:18
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from apis.order_lines.models.process import ProcessModel
from apis.order_lines.schema.process_schema import ProcessSchema
from public.base_view import BaseView


class ProcessView(BaseView):
    url = '/process'

    def __init__(self):
        super(ProcessView, self).__init__()
        self.table_orm = ProcessModel
        self.table_schema = ProcessSchema
