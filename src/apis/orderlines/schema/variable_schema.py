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

from apis.orderlines.models.variable import VariableModel
from public.base_schema import BaseSchema


class VariableSchema(BaseSchema):
    class Meta:
        model = VariableModel
        exclude = ['active']
