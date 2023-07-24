# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : plugin_info_schema.py
# Time       ：2023/7/23 22:19
# Author     ：Y-aong
# version    ：python 3.7
# Description：Plug-in serialization class
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.order_lines.models.plugin_info import PluginInfo


class PluginInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PluginInfo
