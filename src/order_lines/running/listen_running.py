# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : listen_running.py
# Time       ：2023/2/25 15:08
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from order_lines.api.task import TaskInstance
from order_lines.utils.process_action_enum import StatusEnum
from order_lines.variable.variable_handler import VariableHandler


class ListenRunning:
    def __init__(self, process_info):
        self.process_info = process_info
        self.process_id = process_info.get('process_id')
        self.process_instance_id = process_info.get('process_instance_id')
        self.process_name = process_info.get('process_name')
        self.variable_handler = None
        self.error_strategy = {
            'failure': StatusEnum.red.value,
            'retry': StatusEnum.yellow.value,
            'skip': StatusEnum.pink.value
        }

    def insert(self, current_node: dict):
        """
        运行时将任务插入数据库
        :param current_node: 当前正在运行node节点信息
        :return:
        """
        current_task_id = current_node.get('task_id')
        task_name = current_node.get('task_name')
        task_kwargs: dict = current_node.get('method_kwargs')
        task_kwargs = task_kwargs if isinstance(task_kwargs, dict) else {}
        task_kwargs.setdefault('task_id', current_task_id)
        task_kwargs.setdefault('process_id', self.process_id)
        task_kwargs.setdefault('process_name', self.process_name)
        task_kwargs.setdefault('result', current_node.get('result'))
        # 解析参数变量
        self.variable_handler = VariableHandler(current_task_id, task_name, self.process_info)
        task_type = current_node.get('task_type')
        task_kwargs = self.variable_handler.handle_node_params(task_kwargs, task_type)
        current_node['method_kwargs'] = task_kwargs
        task_instance = TaskInstance(current_node, self.process_info)
        task_table_id = task_instance.insert()
        return task_instance, task_table_id

    def update(self, current_node, task_instance, task_instance_id, result_or_error, task_status=None):
        """
        任务运行时任务的运行结果
        :param current_node: 当前正在运行node
        :param task_instance: 任务运行实例对象
        :param task_instance_id: 任务实例id
        :param result_or_error: 任务运行结果或者任务错误信息
        :param task_status: 任务运行结果或者任务状态

        :return:
        """
        assert self.variable_handler, "variable_handler must is not None"
        if task_status == StatusEnum.green.value:
            # 解析返回值
            result = self.variable_handler.handle_node_return(current_node.get('result'), result_or_error)
            table_id = task_instance.update(task_instance_id, StatusEnum.green.value, result=result)
            return table_id
        elif task_status in [StatusEnum.red.value, StatusEnum.pink.value, StatusEnum.orange.value]:
            error = result_or_error.get('error_info')
            table_id = task_instance.update(task_instance_id, task_status, error_info=error, result=result_or_error)
            return table_id
        elif task_status == StatusEnum.yellow.value:
            table_id = task_instance.update(task_instance_id, StatusEnum.yellow.value, error_info=result_or_error)
            return table_id
        else:
            raise ValueError(f'无效的任务状态{task_status}')

    @staticmethod
    def stop_helper(process_instance_id):
        return TaskInstance.stop_helper(process_instance_id)

    @staticmethod
    def get_task_build_time(process_instance_id):
        return TaskInstance.get_task_build_time(process_instance_id)
