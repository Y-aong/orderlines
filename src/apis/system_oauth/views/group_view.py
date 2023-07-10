# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_view.py
# Time       ：2023/7/9 16:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：群组视图
"""
from apis.system_oauth.models import SystemGroup
from apis.system_oauth.schema.group_schema import SystemGroupSchema
from public.base_view import BaseView


class GroupView(BaseView):
    url = '/group'

    def __init__(self):
        super(GroupView, self).__init__()
        self.table_orm = SystemGroup
        self.table_schema = SystemGroupSchema
