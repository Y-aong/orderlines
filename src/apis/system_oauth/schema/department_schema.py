# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : department_schema.py
# Time       ：2023/7/9 16:26
# Author     ：Y-aong
# version    ：python 3.7
# Description：Departmental serialized class
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemDepartment
from apis.system_oauth.schema.user_schema import SystemUserSchema


class SystemDepartmentSchema(SQLAlchemyAutoSchema):
    users = fields.Nested(SystemUserSchema, many=True, dump_only=True, only=('id', 'username'))

    class Meta:
        model = SystemDepartment
        exclude = ['active']
