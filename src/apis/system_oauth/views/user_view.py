# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_view.py
# Time       ：2023/7/9 16:28
# Author     ：Y-aong
# version    ：python 3.7
# Description：用户视图类
"""
from apis.system_oauth.models import SystemUser
from apis.system_oauth.schema.user_schema import SystemUserSchema
from public.base_view import BaseView


class UserView(BaseView):
    url = '/user'

    def __init__(self):
        super(UserView, self).__init__()
        self.table_orm = SystemUser
        self.table_schema = SystemUserSchema
