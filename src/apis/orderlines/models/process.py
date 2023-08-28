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
    process_params = db.Column(db.JSON, comment='process params')
    process_config = db.Column(db.JSON, comment='process other config')
    desc = db.Column(db.String(255), comment='process desc')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='process insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='process update time')
    creator = db.Column(db.String(30), comment='process creator name')
    creator_id = db.Column(db.Integer, comment='process creator id')
    updater = db.Column(db.String(30), comment='process updater name')
    updater_id = db.Column(db.Integer, comment='process updater id')
    # relation
    process_instance = db.relationship('ProcessInstance', backref='base_process')
    task = db.relationship('Task', backref='base_process')
    task_instance = db.relationship('TaskInstance', backref='base_process')


class ProcessInstance(Base):
    __tablename__ = 'base_process_instance'

    process_instance_id = db.Column(db.String(255), unique=True, comment='process run instance id')
    process_name = db.Column(db.String(30), comment='process name')
    process_params = db.Column(db.JSON, comment='process run instance params')
    process_config = db.Column(db.JSON, comment='process run instance config')
    start_time = db.Column(db.DateTime, default=func.now(), comment='process run instance start_time')
    end_time = db.Column(db.DateTime, comment='process run instance end_time')
    runner = db.Column(db.String(40), comment='process run instance runner')
    runner_id = db.Column(db.String(40), comment='process run instance runner id')
    process_error_info = db.Column(db.JSON, comment='process error info')
    process_status = db.Column(db.String(10), comment='process run instance status')
    # relation
    task_instance = db.relationship('TaskInstance', backref='base_process_instance')
    process_id = db.Column(db.String(255), db.ForeignKey('base_process.process_id'), comment='process id')
    run_type = db.Column(db.Enum('schedule', 'trigger'), default='trigger', comment='触发方式')
