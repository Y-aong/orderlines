# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_config_schema.py
# Time       ：2023/8/2 15:17
# Author     ：YangYong
# version    ：python 3.10
# Description：
    配置类序列化类
    base config schema
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.config.models.base_config import BaseConfig


class BaseConfigSchema(SQLAlchemyAutoSchema):
    insert_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    update_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BaseConfig


class DefaultTaskConfigSchema(SQLAlchemyAutoSchema):
    config_name = fields.String()
    config_value = fields.String()
    desc = fields.String()
