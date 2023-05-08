# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_model.py
# Time       ：2023/1/29 21:13
# Author     ：blue_moon
# version    ：python 3.7
# Description：变量模型类
"""
from flask_app.celery_order_lines.models.base_model import Base, db


class VariableModel(Base):
    """
    变量一旦创建不能修改变量名字只可以删除变量重新创建
    # 存入变量是在任务运行时进行进行存入
    # 解析变量是在任务运行时进行解析
    """
    __tablename__ = 'variable'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String(255), comment='流程id')
    process_instance_id = db.Column(db.String(255), comment='流程实例id')
    process_name = db.Column(db.String(50), comment='流程名称')
    task_name = db.Column(db.String(50), comment='任务名称')
    variable_name = db.Column(db.String(50), comment='变量名称')
    # 任务id加variable_name确定唯一的变量
    task_id = db.Column(db.String(255), comment='任务id')
    variable_value = db.Column(db.Text, comment='变量值')
    variable_desc = db.Column(db.String(255), comment='变量描述信息')
    variable_type = db.Column(db.Enum('str', 'int', 'float', 'bool', 'None', 'list', 'dict', ''), comment='变量描述信息')
    # 当变量值为大数据时可以将变量值放在缓存数据库中，variable_value存放id
    is_cache = db.Column(db.SmallInteger, default=0, comment='是否放入缓存')

    @staticmethod
    def get_process_task_name(task_id: str):
        session = Base.get_session()
        instance = session.query(
            VariableModel.process_name,
            VariableModel.task_name
        ).filter(VariableModel.task_id == task_id).first()
        if not instance:
            return None, None
        else:
            process_name, task_name = instance
            return process_name, task_name
