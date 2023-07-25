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

from sqlalchemy import or_

from public.base_model import get_session
from order_lines.utils.process_action_enum import StatusEnum
from apis.order_lines.models import TaskInstanceModel


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
        return TaskInstanceModel.insert_db(TaskInstanceModel, task_data)

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
        return TaskInstanceModel.update_db(TaskInstanceModel, {'id': table_id}, update_data)

    @staticmethod
    def stop_helper(process_instance_id):
        session = get_session()
        task_info = session.query(TaskInstanceModel.task_name, TaskInstanceModel.id).filter(
            TaskInstanceModel.process_instance_id == process_instance_id,
            or_(TaskInstanceModel.task_status == StatusEnum.blue.value,
                TaskInstanceModel.task_status == StatusEnum.grey.value)
        ).all()
        task_names = set()
        for temp in task_info:
            task_name, task_id = temp
            task_names.add(task_name)
            session.query(TaskInstanceModel).filter(
                TaskInstanceModel.id == task_id
            ).update({'task_status': StatusEnum.yellow.value})
        return list(task_names)

    @staticmethod
    def get_task_build_time(process_instance_id):
        """
        获取正在运行中的流程信息,
        Gets information about a running process
        """
        session = get_session()
        task_info = session.query(TaskInstanceModel.task_id, TaskInstanceModel.start_time).filter(
            TaskInstanceModel.process_instance_id == process_instance_id,
            or_(TaskInstanceModel.task_status == StatusEnum.blue.value,
                TaskInstanceModel.task_status == StatusEnum.grey.value))
        result = list()
        for temp in task_info:
            task_id, start_time = temp
            task_info.append({'task_id': task_id, 'start_time': start_time})
        return result
