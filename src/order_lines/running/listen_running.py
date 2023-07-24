# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : listen_running.py
# Time       ：2023/2/25 15:08
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务运行时的处理，主要是对于返回值的处理和参数的解析
    The processing of the task running is mainly the processing of the returned value and the parsing of the parameters
"""
from order_lines.operators.task import TaskInstanceOperator
from public.logger import logger
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
        The task is inserted into the database at run time
        :param current_node: Info about a running node
        :return:task instance, task_table_id
        """
        current_task_id = current_node.get('task_id')
        task_name = current_node.get('task_name')
        task_kwargs: dict = current_node.get('method_kwargs')
        task_kwargs = task_kwargs if isinstance(task_kwargs, dict) else {}
        task_kwargs.setdefault('task_id', current_task_id)
        task_kwargs.setdefault('process_id', self.process_id)
        task_kwargs.setdefault('process_name', self.process_name)
        task_kwargs.setdefault('result', current_node.get('result'))
        # parser parameter variable
        self.variable_handler = VariableHandler(current_task_id, task_name, self.process_info)
        task_type = current_node.get('task_type')
        task_kwargs = self.variable_handler.handle_node_params(task_kwargs, task_type)
        current_node['method_kwargs'] = task_kwargs
        task_instance = TaskInstanceOperator(current_node, self.process_info)
        task_table_id = task_instance.insert()
        return task_instance, task_table_id

    def update(self, current_node, task_instance, task_instance_id, result_or_error, task_status=None):
        """
        任务运行时任务的运行结果
        Task Runtime Running result of a task
        :param current_node: Current running node
        :param task_instance: Task run instance
        :param task_instance_id: Task instance id
        :param result_or_error: Task running result or task error info
        :param task_status: Task running result or task status
        :return:任务id
        """
        assert self.variable_handler, "variable_handler must is not None"
        if task_status == StatusEnum.green.value:
            # 解析返回值
            result = self.variable_handler.handle_node_return(current_node.get('result'), result_or_error)
            logger.info(f'running task_id::{task_instance.task_id}, run result{result}')
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
            raise ValueError(f'Invalid task status:{task_status}')

    @staticmethod
    def stop_helper(process_instance_id):
        return TaskInstanceOperator.stop_helper(process_instance_id)

    @staticmethod
    def get_task_build_time(process_instance_id):
        return TaskInstanceOperator.get_task_build_time(process_instance_id)
