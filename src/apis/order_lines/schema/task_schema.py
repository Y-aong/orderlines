# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_schema.py
# Time       ：2023/7/7 21:56
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务模型序列化类
    Task model serialization class
"""
import json

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.order_lines.models import TaskModel, TaskInstanceModel


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
