# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_schema.py
# Time       ：2023/7/8 15:21
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    变量模型序列化类
    Variable serialization class
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from apis.orderlines.models.variable import Variable
from orderlines.utils.utils import get_variable_value


class VariableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Variable


class VariableInfoSchema(SQLAlchemyAutoSchema):
    variable_key = fields.String()
    variable_value = fields.Function(
        serialize=lambda obj: get_variable_value(obj.variable_value, obj.variable_type)
    )
    variable_type = fields.String()
    variable_desc = fields.String()
    is_cache = fields.Boolean()
