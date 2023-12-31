# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schedule_task.py
# Time       ：2023/8/2 14:28
# Author     ：YangYong
# version    ：python 3.10
# Description：
    定时任务
    schedule task
"""
from sqlalchemy import func

from public.base_model import Base, db


class ScheduleTask(Base):
    __tablename__ = 'base_schedule_task'
    schedule_task_name = db.Column(db.String(128), unique=True, comment='schedule task name')
    process_id = db.Column(db.String(255), unique=True, comment='process id')
    process_name = db.Column(db.String(30), unique=True, comment='process name')
    process_params = db.Column(db.JSON, comment='process params')
    process_config = db.Column(db.JSON, comment='process other config')
    desc = db.Column(db.String(255), comment='process desc')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='update time')

    creator = db.Column(db.String(30), comment='process creator name')
    creator_id = db.Column(db.Integer, comment='process creator id')
    updater = db.Column(db.String(30), comment='process updater name')
    updater_id = db.Column(db.Integer, comment='process updater id')
    # schedule relation
    trigger = db.Column(db.Enum('date', 'interval', 'crontab'), comment='schedule trigger type')
    schedule_plan = db.Column(db.JSON, comment='schedule plan param')
    schedule_plan_id = db.Column(db.Integer, comment='schedule plan id')
    invalid_start_time = db.Column(db.DateTime, comment='invalid start time')
    invalid_end_time = db.Column(db.DateTime, comment='invalid end time')
