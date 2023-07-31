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
import uuid

from apis.orderlines.schema.task_schema import TaskInstanceSchema
from orderlines.utils.process_action_enum import StatusEnum
from apis.orderlines.models import TaskInstance
from public.base_model import get_session


class TaskInstanceOperator:
    def __init__(self, node_info: dict, process_info: dict):
        self.node_info = copy.deepcopy(node_info)
        self.task_id = self.node_info.get('task_id')
        self.process_id = process_info.get('process_id')
        self.process_instance_id = process_info.get('process_instance_id')
        self.session = get_session()

    @property
    def task_instance_id(self):
        return str(uuid.uuid1().hex)

    def insert(self) -> int:
        task_data = dict()
        for key, val in self.node_info.items():
            if hasattr(TaskInstance, key):
                task_data[key] = val

        task_instance_info = TaskInstanceSchema().load(task_data)
        task_instance_info['task_instance_id'] = self.task_instance_id
        task_instance_info['process_id'] = self.process_id
        task_instance_info['process_instance_id'] = self.process_instance_id
        task_instance_info['task_status'] = StatusEnum.grey.value
        task_instance_info = TaskInstanceSchema().load(task_instance_info)
        obj = TaskInstance(**task_instance_info)
        self.session.add(obj)
        self.session.commit()
        return obj.id

    def update(self, table_id, task_status, **kwargs) -> int:
        update_data = dict()
        update_data['end_time'] = datetime.datetime.now()
        update_data['process_instance_id'] = self.process_instance_id
        if task_status == StatusEnum.green.value:
            update_data['task_result'] = kwargs.get('result')
        else:
            update_data['task_result'] = {'status': task_status}
            update_data['task_error_info'] = kwargs.get('error_info')
        update_data['task_status'] = task_status
        return TaskInstance.update_db(TaskInstance, {'id': table_id}, update_data)
