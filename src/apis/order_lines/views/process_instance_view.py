# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_instance_view.py
# Time       ：2023/3/12 13:20
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from apis.order_lines.models.process import ProcessInstanceModel
from apis.order_lines.schema.process_schema import ProcessInstanceSchema
from public.base_view import BaseView


class ProcessInstanceView(BaseView):
    url = '/process_instance'

    def __init__(self):
        super(ProcessInstanceView, self).__init__()
        self.table_orm = ProcessInstanceModel
        self.table_schema = ProcessInstanceSchema
