# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : permission_view.py
# Time       ：2023/7/9 16:42
# Author     ：Y-aong
# version    ：python 3.7
# Description：permission view
"""
from apis.system_oauth.models import SystemPermission
from apis.system_oauth.schema.permission_schema import SystemPermissionSchema
from public.base_view import BaseView


class PermissionView(BaseView):
    url = '/permission'

    def __init__(self):
        super(PermissionView, self).__init__()
        self.table_orm = SystemPermission
        self.table_schema = SystemPermissionSchema
