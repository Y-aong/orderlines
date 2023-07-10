# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_schema.py
# Time       ：2023/7/9 16:15
# Author     ：Y-aong
# version    ：python 3.7
# Description：用户序列化类
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemUser, SystemUserGroupRelation, SystemUserRoleRelation
from public.api_utils.jwt_utils import encrypt_password


class SystemUserSchema(SQLAlchemyAutoSchema):
    password = fields.Function(
        deserialize=lambda value: encrypt_password(value),
        dump_only=True
    )
    create_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = SystemUser


class SystemUserGroupRelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemUserGroupRelation


class SystemUserRoleRelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemUserRoleRelation


# print(encrypt_password('123'))
