# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process.py
# Time       ：2023/7/7 21:48
# Author     ：Y-aong
# version    ：python 3.7
# Description：流程模型类
"""
from sqlalchemy import func

from public.base_model import Base, db


class ProcessModel(Base):
    __tablename__ = 'process'

    process_id = db.Column(db.String(255), unique=True, comment='流程id')
    process_name = db.Column(db.String(30), unique=True, comment='流程名称')
    process_params = db.Column(db.Text, comment='流程参数信息')
    process_config = db.Column(db.Text, comment='流程其他配置')
    desc = db.Column(db.String(255), comment='流程描述信息')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='流程插入时间')
    update_time = db.Column(db.DateTime, comment='流程更新时间')
    creator = db.Column(db.String(30), comment='流程创建者')
    updater = db.Column(db.String(30), comment='流程修改者')


class ProcessInstanceModel(Base):
    __tablename__ = 'process_instance'
    process_id = db.Column(db.String(255), comment='流程id')
    process_instance_id = db.Column(db.String(255), unique=True, comment='流程运行id')
    process_name = db.Column(db.String(30), comment='流程实例名称')
    process_params = db.Column(db.Text, comment='流程实例参数信息')
    process_config = db.Column(db.Text, comment='流程实例其他配置')
    start_time = db.Column(db.DateTime, default=func.now(), comment='流程实例开始时间')
    end_time = db.Column(db.DateTime, comment='流程实例结束时间')
    runner = db.Column(db.String(40), comment='流程实例运行者')
    runner_id = db.Column(db.String(40), comment='流程实例运行者id')
    process_error_info = db.Column(db.Text, comment='流程错误信息')
    process_status = db.Column(db.String(10), comment='流程实例运行状态')
