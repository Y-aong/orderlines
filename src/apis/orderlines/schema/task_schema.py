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

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from apis.orderlines.models import Task, TaskInstance


class TaskInstanceSchema(SQLAlchemyAutoSchema):
    task_id = auto_field()
    process_id = auto_field()
    process_instance_id = auto_field()
    start_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TaskInstance
        exclude = ['active']


class TaskSchema(SQLAlchemyAutoSchema):
    insert_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    update_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    process_id = auto_field()
    task_instance = fields.Nested(TaskInstanceSchema, many=True, dump_only=True)

    class Meta:
        model = Task
        exclude = ['active']