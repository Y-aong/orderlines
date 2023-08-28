# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable.py
# Time       ：2023/1/29 21:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    变量模型类
    Variable model class
"""
from sqlalchemy import func

from public.base_model import Base, db


class Variable(Base):
    """变量配置表"""
    __tablename__ = 'base_variable'

    process_id = db.Column(db.String(255), comment='process id')
    process_name = db.Column(db.String(50), comment='process name')
    # process_instance_id + variable_name确定唯一的变量
    variable_key = db.Column(db.String(255), comment='variable key')
    variable_value = db.Column(db.Text, comment='variable value')
    variable_desc = db.Column(db.String(255), comment='variable desc info')
    variable_type = db.Column(db.Enum('str', 'int', 'float', 'bool', 'None', 'list', 'dict'), comment='variable type')
    # 当变量值为大数据时可以将变量值放在缓存数据库中，variable_value存放id
    # When the variable value is large data,
    # the variable value can be placed in the cache database, and variable_value stores the id
    is_cache = db.Column(db.Boolean, default=False, comment='is cache')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='update time')
    creator_name = db.Column(db.String(64), comment='creator name')
    creator_id = db.Column(db.Integer, comment='creator id')
    updator_name = db.Column(db.String(64), comment='updator name')
    updator_id = db.Column(db.Integer, comment='updator name')


class VariableInstance(Base):
    """
    变量一旦创建不能修改变量名字只可以删除变量重新创建
    存入变量是在任务运行时进行进行存入
    解析变量是在任务运行时进行解析
    Once a variable is created, variable name cannot be modified. You can only delete the variable and create it again
    Stored variables are stored at task runtime
    Parsed variables are parsed at task runtime
    """
    __tablename__ = 'base_variable_instance'

    process_id = db.Column(db.String(255), comment='process id')
    process_instance_id = db.Column(db.String(255), comment='process instance id')
    process_name = db.Column(db.String(50), comment='process name')
    # variable relation
    variable_key = db.Column(db.String(50), comment='variable key')
    variable_value = db.Column(db.Text, comment='variable value')
    variable_desc = db.Column(db.String(255), comment='variable desc info')
    variable_type = db.Column(db.Enum('str', 'int', 'float', 'bool', 'None', 'list', 'dict'), comment='variable type')
    # 当变量值为大数据时可以将变量值放在缓存数据库中，variable_value存放id
    # When the variable value is large data,
    # the variable value can be placed in the cache database, and variable_value stores the id
    is_cache = db.Column(db.Boolean, default=False, comment='is cache')
