# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_permission_schema.py
# Time       ：2023/7/17 22:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：用户权限序列化类
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class SystemUserPermissionSchema(SQLAlchemyAutoSchema):
    method = fields.String()
    path = fields.String()
    name = fields.String()
    user_id = fields.Integer()
    username = fields.String()
