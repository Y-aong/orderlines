# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : variable_view.py
# Time       ：2023/8/28 15:07
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines变量视图
"""
from apis.orderlines.models import Variable
from apis.orderlines.schema.variable_schema import VariableSchema
from public.base_view import BaseView


class VariableView(BaseView):
    url = '/variable'

    def __init__(self):
        super(VariableView, self).__init__()
        self.table_orm = Variable
        self.table_schema = VariableSchema
