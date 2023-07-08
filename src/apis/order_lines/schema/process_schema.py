# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_schema.py
# Time       ：2023/3/12 10:26
# Author     ：Y-aong
# version    ：python 3.7
# Description：序列化类
"""
import json

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.order_lines.models.process import ProcessModel, ProcessInstanceModel


class ProcessSchema(SQLAlchemyAutoSchema):
    process_params = fields.Function(
        serialize=lambda obj: json.loads(obj.process_params) if obj.process_params else None,
        deserialize=lambda value: json.dumps(value)
    )
    process_config = fields.Function(
        serialize=lambda obj: json.loads(obj.process_config) if obj.process_config else None,
        deserialize=lambda value: json.dumps(value)
    )

    class Meta:
        model = ProcessModel


class ProcessInstanceSchema(SQLAlchemyAutoSchema):
    process_params = fields.Function(
        serialize=lambda obj: json.loads(obj.process_params) if obj.process_params else None,
        deserialize=lambda value: json.dumps(value)
    )
    process_config = fields.Function(
        serialize=lambda obj: json.loads(obj.process_config) if obj.process_config else None,
        deserialize=lambda value: json.dumps(value)
    )

    class Meta:
        model = ProcessInstanceModel
