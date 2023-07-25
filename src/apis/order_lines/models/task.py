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


class TaskModel(Base):
    __tablename__ = 'base_task'

    task_id = db.Column(db.String(255), comment='task id')
    prev_id = db.Column(db.String(255), comment='task prev task_id')
    next_id = db.Column(db.String(255), comment='task next task_id')
    task_name = db.Column(db.String(50), comment='task name')
    method_name = db.Column(db.String(50), comment='task run method name')
    method_kwargs = db.Column(db.Text, comment='task run parma')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='task insert time')
    update_time = db.Column(db.DateTime, comment='task update time')
    creator = db.Column(db.String(30), comment='task creator')
    updater = db.Column(db.String(30), comment='task updater')
    task_type = db.Column(db.Enum('common', 'process_control', 'parallel', 'group', 'start', 'end'),
                          comment='task type')
    task_module = db.Column(db.String(50), comment='task module')
    task_config = db.Column(db.String(255), comment='task config')
    desc = db.Column(db.String(255), comment='task desc')
    process_id = db.Column(db.String(255), comment='process id')


class TaskInstanceModel(Base):
    __tablename__ = 'base_task_instance'

    task_id = db.Column(db.String(255), comment='task id')
    task_instance_id = db.Column(db.String(255), comment='task run id')
    task_name = db.Column(db.String(50), comment='task name')
    method_name = db.Column(db.String(20), comment='task run method name')
    task_kwargs = db.Column(db.Text, comment='task run param')
    task_status = db.Column(db.String(20), comment='task run instance status')
    start_time = db.Column(db.DateTime, default=func.now(), comment='task instance start time')
    end_time = db.Column(db.DateTime, comment='task instance end time')
    runner = db.Column(db.String(40), comment='task  runner')
    runner_id = db.Column(db.String(40), comment='task runner id')
    task_result = db.Column(db.Text, comment='task return')
    task_error_info = db.Column(db.Text, comment='task run error info')
    process_instance_id = db.Column(db.String(255), comment='process instance id')
