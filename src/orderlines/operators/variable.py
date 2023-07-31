# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable.py
# Time       ：2023/1/29 21:30
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    变量模块操作类
    Variable Model Operator
"""
from typing import Any

from apis.orderlines.models import VariableModel


class VariableModelOperator:
    def __init__(self, task_id: str, variable_name: str):
        self.task_id = task_id
        self.variable_name = variable_name

    def insert_db(self, process_info, variable_value, variable_info, task_name):
        variable_data = dict()
        variable_data['task_id'] = self.task_id
        variable_data['task_name'] = task_name
        variable_data['process_id'] = process_info.get('process_id')
        variable_data['process_instance_id'] = process_info.get('process_instance_id')
        variable_data['process_name'] = process_info.get('process_name')
        variable_data['variable_name'] = self.variable_name
        variable_data['variable_value'] = variable_value
        variable_data.update(variable_info)
        variable_data.setdefault('is_cache', False)
        return VariableModel.insert_db(VariableModel, variable_data)

    @staticmethod
    def update_db(process_instance_id: str, task_name: str, variable_value: Any, **kwargs) -> int:
        """
        修改变量信息。已创建的变量名不能修改
        Modify variable information. A created variable name cannot be modified
        :param process_instance_id:
        :param task_name:
        :param variable_value: 变量值
        :param kwargs: 变量描述信息
        :return: variable_id
        """
        variable_info = {'variable_value': variable_value, 'task_name': task_name}
        variable_info.update(kwargs)
        # todo 对于is_cache进行处理
        filter_data = {'process_instance_id': process_instance_id, 'variable_name': kwargs.get('variable_name')}
        return VariableModel.update_db(VariableModel, filter_data, variable_info)

    @staticmethod
    def select_data(process_instance_id, variable_name):
        """
        获取流程中的变量数据，一个流程中变量名是唯一的
        Gets data about variables in a process where variable names are unique
        :param process_instance_id:流程实例id
        :param variable_name:变量名称
        :return:
        """
        filter_data = {'variable_name': variable_name, 'process_instance_id': process_instance_id}
        return VariableModel.select_db(VariableModel, filter_data)
