# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : custom_schema.py
# Time       ：2023/8/9 18:40
# Author     ：YangYong
# version    ：python 3.10
# Description：
    自定义外键软删除序列化
"""
import typing
from marshmallow.fields import Nested


class CustomNested(Nested):
    def serialize(
            self,
            attr: str,
            obj: typing.Any,
            accessor: typing.Any = None,
            **kwargs
    ) -> typing.Union[dict, list]:
        result = super(CustomNested, self).serialize(attr, obj, accessor)
        if isinstance(result, list):
            result = [item for item in result if item.get('active')]
        elif isinstance(result, dict) and not result.get('active'):
            result = {}

        return result
