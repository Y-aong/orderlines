# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : tasks.py
# Time       ：2023/1/10 22:35
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务节点操作api
    task instance operator
"""
import copy
import datetime
import json
import uuid

from order_lines.utils.process_action_enum import StatusEnum
from apis.order_lines.models import TaskInstance


class TaskInstanceOperator:
    def __init__(self, node_info: dict, process_info: dict):
        self.node_info = copy.deepcopy(node_info)
        self.task_id = node_info.get('task_id')
        self.task_params = node_info.get('method_kwargs')
        self.method_name = node_info.get('method_name')
        self.task_name = node_info.get('task_name')
        self.process_id = process_info.get('process_id')
        self.process_instance_id = process_info.get('process_instance_id')

    @property
    def task_instance_id(self):
        return uuid.uuid1()

    def insert(self) -> int:
        task_data = dict()
        task_data['task_kwargs'] = json.dumps(self.task_params)
        task_data['method_name'] = self.method_name
        task_data['task_name'] = self.task_name
        task_data['task_id'] = self.task_id
        task_data['task_instance_id'] = self.task_instance_id
        task_data['process_id'] = self.process_id
        task_data['process_instance_id'] = self.process_instance_id
        task_data['start_time'] = datetime.datetime.now()
        task_data['task_status'] = StatusEnum.grey.value
        return TaskInstance.insert_db(TaskInstance, task_data)

    def update(self, table_id, task_status, **kwargs) -> int:
        update_data = dict()
        update_data['end_time'] = datetime.datetime.now()
        update_data['process_instance_id'] = self.process_instance_id
        if task_status == StatusEnum.green.value:
            update_data['task_result'] = json.dumps(kwargs.get('result'))
        else:
            update_data['task_result'] = json.dumps({'status': task_status})
            update_data['task_error_info'] = json.dumps(kwargs.get('error_info'))
        update_data['task_status'] = task_status
        return TaskInstance.update_db(TaskInstance, {'id': table_id}, update_data)
