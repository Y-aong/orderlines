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
from marshmallow import fields
from apis.config.models.plugin_info import PluginInfo


class PluginInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PluginInfo


class PluginNodeInfoSchema(SQLAlchemyAutoSchema):
    type = fields.Function(serialize=lambda obj: obj.node_type)
    title = fields.Function(serialize=lambda obj: obj.title)
    background = fields.String()
    class_name = fields.String()
    text = fields.Function(
        serialize=lambda obj: obj.method_desc
    )
    method_name = fields.String()
    version = fields.String()


class NodeParamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PluginInfo
        fields = ['parameters']


class NodeResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PluginInfo
        fields = ['return_value']


class NodeConfigSchema(SQLAlchemyAutoSchema):
    task_name = fields.Function(lambda obj: obj.method_desc)
    version = fields.String()
    desc = fields.Function(lambda obj: obj.method_desc)
    method_name = fields.String()
