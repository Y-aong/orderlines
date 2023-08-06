# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_permission_schema.py
# Time       ：2023/7/17 22:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    用户权限关系序列化类
    User permission serialized class
"""
from marshmallow import fields

from public.base_schema import BaseSchema


class SystemUserPermissionSchema(BaseSchema):
    method = fields.String()
    path = fields.String()
    name = fields.String()
    user_id = fields.Integer()
    username = fields.String()
