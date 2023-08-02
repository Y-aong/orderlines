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
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.orderlines.models.schedule_task import ScheduleTask


class ScheduleTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ScheduleTask
        exclude = ['active']
