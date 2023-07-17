# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_schema.py
# Time       ：2023/7/9 16:23
# Author     ：Y-aong
# version    ：python 3.7
# Description：群组序列化类
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemGroup


class SystemGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemGroup
        exclude = ['active']
