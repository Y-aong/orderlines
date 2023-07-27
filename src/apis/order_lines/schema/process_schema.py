# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_schema.py
# Time       ：2023/3/12 10:26
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程序列化类
    process serialization class
"""
import json

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.order_lines.models.process import Process, ProcessInstance


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
        model = Process


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
        model = ProcessInstance


class ProcessInstanceExportSchema(SQLAlchemyAutoSchema):
    process_id = fields.String()
    process_name = fields.String()
    process_params = fields.Function(serialize=lambda obj: json.loads(obj.process_params))
    process_config = fields.Function(serialize=lambda obj: json.loads(obj.process_config))
    start_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    runner = fields.String()
    runner_id = fields.Integer()
    process_error_info = fields.String()
    process_status = fields.String()
    task_name = fields.String()
    task_id = fields.String()
    method_name = fields.String()
    task_kwargs = fields.Function(serialize=lambda obj: json.loads(obj.task_kwargs) if obj.task_kwargs else None)
    task_result = fields.Function(serialize=lambda obj: json.loads(obj.task_result) if obj.task_result else None)
    task_status = fields.String()
