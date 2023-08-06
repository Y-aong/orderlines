# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schedule_task_schema.py
# Time       ：2023/8/2 15:18
# Author     ：YangYong
# version    ：python 3.10
# Description：
    定时任务序列化类
    schedule task schema
"""
from typing import Union

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pydantic import BaseModel, Field

from apis.orderlines.models.schedule_task import ScheduleTask


class ScheduleTaskSchema(SQLAlchemyAutoSchema):
    insert_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    update_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ScheduleTask
        exclude = ['active']


class CreateScheduleTask(BaseModel):
    id: Union[int, None] = Field(default=None, description='定时任务id')
    trigger: str = Field(description='定时类型')
    job_id: str = Field(description='流程id也是定时计划id')
    schedule_task_name: str = Field(description='流程名称， 任务名称')
    schedule_plan: dict = Field(description='定时计划参数')
