# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task.py
# Time       ：2023/1/11 21:03
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    task 模型类
    task model
"""

from sqlalchemy import func

from public.base_model import Base, db


class Task(Base):
    __tablename__ = 'base_task'

    task_id = db.Column(db.String(255), unique=True, comment='task id')
    prev_id = db.Column(db.String(255), comment='task prev task_id')
    next_id = db.Column(db.String(255), comment='task next task_id')
    task_name = db.Column(db.String(50), comment='task name')
    method_name = db.Column(db.String(50), comment='task run method name')
    method_kwargs = db.Column(db.JSON, comment='task run parma')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='update time')
    creator = db.Column(db.String(30), comment='task creator name')
    creator_id = db.Column(db.Integer, comment='task creator id')
    updater = db.Column(db.String(30), comment='task updater name')
    updater_id = db.Column(db.Integer, comment='task updater id')
    task_type = db.Column(
        db.Enum('common', 'process_control', 'parallel', 'group', 'start', 'end'), comment='task type')
    task_module = db.Column(db.String(50), comment='task module')
    module_version = db.Column(db.String(64), default='1.0.0.1', comment='module version')
    task_config = db.Column(db.JSON, comment='task config')
    result_config = db.Column(db.JSON, comment='result config')
    desc = db.Column(db.String(255), comment='task desc')
    # relation
    process_id = db.Column(db.String(255), db.ForeignKey('base_process.process_id'), comment='process id')
    task_instance = db.relationship('TaskInstance', backref='base_task')


class TaskInstance(Base):
    __tablename__ = 'base_task_instance'

    task_instance_id = db.Column(db.String(255), comment='task run id')
    task_name = db.Column(db.String(50), comment='task name')
    task_type = db.Column(
        db.Enum('common', 'process_control', 'parallel', 'group', 'start', 'end'), comment='task type')
    task_module = db.Column(db.String(50), comment='task module')
    task_config = db.Column(db.JSON, comment='task config')
    method_name = db.Column(db.String(20), comment='task run method name')
    method_kwargs = db.Column(db.JSON, comment='task run param')
    task_status = db.Column(db.String(20), comment='task run instance status')
    start_time = db.Column(db.DateTime, default=func.now(), comment='task instance start time')
    end_time = db.Column(db.DateTime, comment='task instance end time')
    runner = db.Column(db.String(40), comment='task  runner')
    runner_id = db.Column(db.String(40), comment='task runner id')
    task_result = db.Column(db.JSON, comment='task return')
    task_error_info = db.Column(db.JSON, comment='task run error info')
    result_config = db.Column(db.JSON(255), comment='result config')
    task_desc = db.Column(db.String(255), comment='task desc')
    # relation
    process_id = db.Column(db.String(255), db.ForeignKey('base_process.process_id'), comment='process id')
    process_instance_id = db.Column(
        db.String(255), db.ForeignKey('base_process_instance.process_instance_id'), comment='process instance id')
    task_id = db.Column(db.String(255), db.ForeignKey('base_task.task_id'), comment='task id')
