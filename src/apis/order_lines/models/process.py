# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process.py
# Time       ：2023/7/7 21:48
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    process 模型类
    process model class
"""
from sqlalchemy import func

from public.base_model import Base, db


class Process(Base):
    __tablename__ = 'base_process'

    process_id = db.Column(db.String(255), unique=True, comment='process id')
    process_name = db.Column(db.String(30), unique=True, comment='process name')
    process_params = db.Column(db.Text, comment='process params')
    process_config = db.Column(db.Text, comment='process other config')
    desc = db.Column(db.String(255), comment='process desc')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='process insert time')
    update_time = db.Column(db.DateTime, comment='process update time')
    creator = db.Column(db.String(30), comment='process creator')
    updater = db.Column(db.String(30), comment='process updater')


class ProcessInstance(Base):
    __tablename__ = 'base_process_instance'
    process_id = db.Column(db.String(255), comment='process id')
    process_instance_id = db.Column(db.String(255), unique=True, comment='process run instance id')
    process_name = db.Column(db.String(30), comment='process name')
    process_params = db.Column(db.JSON, comment='process run instance params')
    process_config = db.Column(db.JSON, comment='process run instance config')
    start_time = db.Column(db.DateTime, default=func.now(), comment='process run instance start_time')
    end_time = db.Column(db.DateTime, comment='process run instance end_time')
    runner = db.Column(db.String(40), comment='process run instance runner')
    runner_id = db.Column(db.String(40), comment='process run instance runner id')
    process_error_info = db.Column(db.Text, comment='process error info')
    process_status = db.Column(db.String(10), comment='process run instance status')
