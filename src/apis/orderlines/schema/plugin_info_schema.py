# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : plugin_info_schema.py
# Time       ：2023/7/23 22:19
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    插件序列化类
    Plug-in serialization class
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.orderlines.models.plugin_info import PluginInfo


class PluginInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PluginInfo
