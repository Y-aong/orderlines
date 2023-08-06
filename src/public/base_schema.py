# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_schema.py
# Time       ：2023/8/6 14:27
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
import typing

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class BaseSchema(SQLAlchemyAutoSchema):
    def __init__(self):
        super(BaseSchema, self).__init__()

    def dump(self, obj: typing.Any, *, many: typing.Union[None, bool] = None):
        if not obj and not many:
            return {}
        elif not obj and many:
            return [{}]
        else:
            return super().dump(obj, many=many)
