# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_schema.py
# Time       ：2023/7/8 15:21
# Author     ：Y-aong
# version    ：python 3.7
# Description：变量序列化类
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.order_lines.models.variable import Variable


class VariableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Variable
