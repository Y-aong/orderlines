# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : permission_schema.py
# Time       ：2023/7/9 16:24
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    权限序列化类
    Permission serialized class
"""

from apis.system_oauth.models import SystemPermission
from public.base_schema import BaseSchema


class SystemPermissionSchema(BaseSchema):
    class Meta:
        model = SystemPermission
        exclude = ['active']
