# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderline_models.py
# Time       ：2023/1/11 21:03
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import datetime

from flask_app.order_lines_app.models.base_model import Base, db


class ProcessModel(Base):
    __tablename__ = 'process'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String(255), unique=True, comment='流程id')
    process_name = db.Column(db.String(30), unique=True, comment='流程名称')
    process_params = db.Column(db.Text, comment='流程参数信息')
    process_config = db.Column(db.Text, comment='流程其他配置')
    desc = db.Column(db.String(255), comment='流程描述信息')
    insert_time = db.Column(db.DateTime, default=datetime.datetime.utcnow(), comment='流程插入时间')
    update_time = db.Column(db.DateTime, comment='流程更新时间')
    creator = db.Column(db.String(30), comment='流程创建者')
    updater = db.Column(db.String(30), comment='流程修改者')


class ProcessInstanceModel(Base):
    __tablename__ = 'process_instance'
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String(255), comment='流程id')
    process_instance_id = db.Column(db.String(255), unique=True, comment='流程运行id')
    process_name = db.Column(db.String(30), comment='流程实例名称')
    process_params = db.Column(db.Text, comment='流程实例参数信息')
    process_config = db.Column(db.Text, comment='流程实例其他配置')
    start_time = db.Column(db.DateTime, comment='流程实例开始时间')
    end_time = db.Column(db.DateTime, comment='流程实例结束时间')
    runner = db.Column(db.String(40), comment='流程实例运行者')
    runner_id = db.Column(db.String(40), comment='流程实例运行者id')
    process_error_info = db.Column(db.Text, comment='流程错误信息')
    process_status = db.Column(db.String(10), comment='流程实例运行状态')


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255), comment='任务id')
    prev_id = db.Column(db.String(255), comment='任务上一个task_id')
    next_id = db.Column(db.String(255), comment='任务下一个task_id')
    task_name = db.Column(db.String(50), comment='任务名称')
    method_name = db.Column(db.String(20), comment='任务运行函数名称')
    method_kwargs = db.Column(db.Text, comment='任务运行参数')
    insert_time = db.Column(db.DateTime, default=datetime.datetime.utcnow(), comment='任务插入时间')
    update_time = db.Column(db.DateTime, comment='任务更新时间')
    creator = db.Column(db.String(30), comment='任务创建者')
    updater = db.Column(db.String(30), comment='任务修改者')
    task_type = db.Column(db.Enum('common', 'process_control', 'parallel', 'group', 'start', 'end'), comment='任务类型')
    task_module = db.Column(db.String(50), comment='任务所属模块')
    task_config = db.Column(db.String(255), comment='任务配置信息')
    desc = db.Column(db.String(255), comment='任务描述信息')
    process_id = db.Column(db.String(255), comment='流程id')


class TaskInstanceModel(Base):
    __tablename__ = 'task_instance'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255), comment='任务id')
    task_instance_id = db.Column(db.String(255), comment='任务运行id')
    task_name = db.Column(db.String(50), comment='任务名称')
    method_name = db.Column(db.String(20), comment='任务运行函数名称')
    task_kwargs = db.Column(db.Text, comment='任务运行参数')
    task_status = db.Column(db.String(20), comment='任务实例运行状态')
    start_time = db.Column(db.DateTime, comment='任务实例开始时间')
    end_time = db.Column(db.DateTime, comment='任务实例结束时间')
    runner = db.Column(db.String(40), comment='任务实例运行者')
    runner_id = db.Column(db.String(40), comment='任务实例运行者id')
    task_result = db.Column(db.Text, comment='任务返回值')
    task_error_info = db.Column(db.Text, comment='任务运行错误信息')
    process_instance_id = db.Column(db.String(255), comment='流程实例id')
