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
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from apis.orderlines.models.process import Process, ProcessInstance
from apis.orderlines.schema.task_schema import TaskInstanceSchema, TaskSchema


class ProcessInstanceSchema(SQLAlchemyAutoSchema):
    process_id = auto_field()
    task_instance = fields.Nested(TaskInstanceSchema, many=True, dump_only=True)
    start_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ProcessInstance
        exclude = ['active']


class ProcessSchema(SQLAlchemyAutoSchema):
    process_instance = fields.Nested(ProcessInstanceSchema, many=True, dump_only=True)
    task = fields.Nested(TaskSchema, many=True, dump_only=True)
    insert_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    update_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Process
        exclude = ['active']


class ProcessRunningSchema(SQLAlchemyAutoSchema):
    task = fields.Nested(TaskSchema, many=True, dump_only=True)

    class Meta:
        model = Process
        exclude = ['active', 'id', 'update_time', 'insert_time']


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
    method_kwargs = fields.Function(serialize=lambda obj: json.loads(obj.method_kwargs) if obj.method_kwargs else None)
    task_result = fields.Function(serialize=lambda obj: json.loads(obj.task_result) if obj.task_result else None)
    task_status = fields.String()
