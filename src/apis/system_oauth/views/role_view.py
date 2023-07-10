# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : role_view.py
# Time       ：2023/7/9 16:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：角色视图
"""
from apis.system_oauth.models import SystemRole
from apis.system_oauth.schema.role_schema import SystemRoleSchema
from public.base_view import BaseView


class RoleView(BaseView):
    url = '/role'

    def __init__(self):
        super(RoleView, self).__init__()
        self.table_orm = SystemRole
        self.table_schema = SystemRoleSchema
