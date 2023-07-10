# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : department_schema.py
# Time       ：2023/7/9 16:26
# Author     ：Y-aong
# version    ：python 3.7
# Description：部门序列化类
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemDepartment


class SystemDepartmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemDepartment
