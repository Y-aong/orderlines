# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : role_schema.py
# Time       ：2023/7/9 16:25
# Author     ：Y-aong
# version    ：python 3.7
# Description：角色序列化类
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemRole


class SystemRoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemRole
