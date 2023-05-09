# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_schema.py
# Time       ：2023/3/12 10:26
# Author     ：blue_moon
# version    ：python 3.7
# Description：序列化类
"""
import json

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from flask_app.celery_order_lines.models.order_line_models import *


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


class TaskSchema(SQLAlchemyAutoSchema):
    method_kwargs = fields.Function(
        serialize=lambda obj: json.loads(obj.method_kwargs) if obj.method_kwargs else None,
        deserialize=lambda value: json.dumps(value)
    )
    task_config = fields.Function(
        serialize=lambda obj: json.loads(obj.task_config) if obj.task_config else None,
        deserialize=lambda value: json.dumps(value)
    )

    class Meta:
        model = TaskModel


class TaskInstanceSchema(SQLAlchemyAutoSchema):
    method_kwargs = fields.Function(
        serialize=lambda obj: json.loads(obj.method_kwargs) if obj.method_kwargs else {},
        deserialize=lambda value: json.dumps(value)
    )
    task_config = fields.Function(
        serialize=lambda obj: json.loads(obj.task_config) if obj.task_config else {},
        deserialize=lambda value: json.dumps(value)
    )

    class Meta:
        model = TaskInstanceModel
