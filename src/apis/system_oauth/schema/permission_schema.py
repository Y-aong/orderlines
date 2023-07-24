# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : permission_schema.py
# Time       ：2023/7/9 16:24
# Author     ：Y-aong
# version    ：python 3.7
# Description：Permission serialized class
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemPermission


class SystemPermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemPermission
        exclude = ['active']
