# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task.py
# Time       ：2023/1/11 21:03
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务模型类
"""

from sqlalchemy import func

from public.base_model import Base, db


class TaskModel(Base):
    __tablename__ = 'tasks'

    task_id = db.Column(db.String(255), comment='任务id')
    prev_id = db.Column(db.String(255), comment='任务上一个task_id')
    next_id = db.Column(db.String(255), comment='任务下一个task_id')
    task_name = db.Column(db.String(50), comment='任务名称')
    method_name = db.Column(db.String(50), comment='任务运行函数名称')
    method_kwargs = db.Column(db.Text, comment='任务运行参数')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='任务插入时间')
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
    task_id = db.Column(db.String(255), comment='任务id')
    task_instance_id = db.Column(db.String(255), comment='任务运行id')
    task_name = db.Column(db.String(50), comment='任务名称')
    method_name = db.Column(db.String(20), comment='任务运行函数名称')
    task_kwargs = db.Column(db.Text, comment='任务运行参数')
    task_status = db.Column(db.String(20), comment='任务实例运行状态')
    start_time = db.Column(db.DateTime, default=func.now(), comment='任务实例开始时间')
    end_time = db.Column(db.DateTime, comment='任务实例结束时间')
    runner = db.Column(db.String(40), comment='任务实例运行者')
    runner_id = db.Column(db.String(40), comment='任务实例运行者id')
    task_result = db.Column(db.Text, comment='任务返回值')
    task_error_info = db.Column(db.Text, comment='任务运行错误信息')
    process_instance_id = db.Column(db.String(255), comment='流程实例id')
