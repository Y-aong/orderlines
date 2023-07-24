# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable.py
# Time       ：2023/1/29 21:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：Variable model class
"""
from public.base_model import Base, db


class VariableModel(Base):
    """
    变量一旦创建不能修改变量名字只可以删除变量重新创建
    存入变量是在任务，运行时进行进行存入
    解析变量是在任务 运行时进行解析
    Once a variable is created, the variable name cannot be modified. You can only delete the variable and create it again
    Stored variables are stored at task runtime
    Parsed variables are parsed at task runtime
    """
    __tablename__ = 'base_variable'

    process_id = db.Column(db.String(255), comment='process id')
    process_instance_id = db.Column(db.String(255), comment='process instance id')
    process_name = db.Column(db.String(50), comment='process name')
    task_name = db.Column(db.String(50), comment='task name')
    variable_name = db.Column(db.String(50), comment='variable name')
    # task id加variable_name确定唯一的变量
    task_id = db.Column(db.String(255), comment='task id')
    variable_value = db.Column(db.Text, comment='variable value')
    variable_desc = db.Column(db.String(255), comment='variable desc info')
    variable_type = db.Column(
        db.Enum('str', 'int', 'float', 'bool', 'None', 'list', 'dict', ''), comment='variable type')
    # 当变量值为大数据时可以将变量值放在缓存数据库中，variable_value存放id
    # When the variable value is large data,
    # the variable value can be placed in the cache database, and variable_value stores the id
    is_cache = db.Column(db.SmallInteger, default=0, comment='is cache')

    @staticmethod
    def get_process_task_name(task_id: str):
        session = Base.get_session()
        instance = session.query(
            VariableModel.process_name, VariableModel.task_name
        ).filter(VariableModel.task_id == task_id).first()
        if not instance:
            return None, None
        else:
            process_name, task_name = instance
            return process_name, task_name
