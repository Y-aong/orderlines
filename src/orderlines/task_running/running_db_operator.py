# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : running_db_operator.py
# Time       ：2023/8/1 14:58
# Author     ：YangYong
# version    ：python 3.10
# Description：
    运行时的数据库操作
    db operator on running
"""
import json
import uuid
from datetime import datetime

from apis.orderlines.models import ProcessInstance, TaskInstance
from apis.orderlines.schema.process_schema import ProcessInstanceSchema
from apis.orderlines.schema.task_schema import TaskInstanceSchema
from orderlines.utils.orderlines_enum import ProcessStatus, TaskStatus
from public.base_model import get_session


class RunningDBOperator:
    def __init__(self, process_instance_id: str, process_id: str):
        self.process_instance_id = process_instance_id
        self.process_id = process_id
        self.session = get_session()

    def process_instance_insert(self, process_info: dict, dry=False) -> None:
        if not dry:
            process_instance_info = {
                'process_status': ProcessStatus.grey.value
            }
            for key, val in process_info.items():
                if hasattr(ProcessInstance, key):
                    process_instance_info.setdefault(key, val)
            process_instance_info = ProcessInstanceSchema().load(process_instance_info)
            obj = ProcessInstance(**process_instance_info)
            self.session.add(obj)
            self.session.commit()

    def process_instance_update(
            self,
            process_status: ProcessStatus,
            error_info=None,
            dry=False
    ) -> None:
        if not dry:
            process_instance_info = {
                'process_status': process_status,
                'process_error_info': json.dumps(error_info) if isinstance(error_info, dict) else error_info
            }
            if process_status in ['SUCCESS', 'FAILURE', 'STOP']:
                process_instance_info['end_time'] = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            self.session.query(ProcessInstance).filter(
                ProcessInstance.process_instance_id == self.process_instance_id).update(process_instance_info)
            self.session.commit()

    def task_instance_insert(self, task_node: dict, dry=False) -> str:
        if not dry:
            task_instance_id = str(uuid.uuid1().hex)
            task_instance_info = {
                'process_id': self.process_id,
                'process_instance_id': self.process_instance_id,
                'task_instance_id': task_instance_id,
                'task_status': TaskStatus.green.value
            }
            for key, val in task_node.items():
                if hasattr(TaskInstance, key) and key != 'id':
                    task_instance_info.setdefault(key, val)
            task_instance_info = TaskInstanceSchema().load(task_instance_info)
            obj = TaskInstance(**task_instance_info)
            self.session.add(obj)
            self.session.commit()
            return task_instance_id

    def task_instance_update(
            self,
            task_instance_id: str,
            task_status: TaskStatus,
            result: dict = None,
            error_info: dict = None,
            dry=False
    ) -> None:
        if not dry:
            task_instance_info = {
                'task_status': task_status,
                'task_result': json.dumps(result) if isinstance(result, dict) else result,
                'task_error_info': json.dumps(error_info) if isinstance(error_info, dict) else error_info
            }
            if task_status not in ['PENDING', 'RUNNING']:
                task_instance_info['end_time'] = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            self.session.query(TaskInstance).filter(
                TaskInstance.task_instance_id == task_instance_id).update(task_instance_info)
            self.session.commit()

    def process_instance_is_stop_or_paused(self, dry=False) -> bool:
        if dry:
            return False, False
        obj = self.session.query(ProcessInstance).filter(
            ProcessInstance.process_instance_id == self.process_instance_id).first()
        self.session.commit()
        instance = ProcessInstanceSchema().dump(obj)
        instance_status = instance.get('process_status')
        return instance_status == ProcessStatus.yellow.value, instance_status == ProcessStatus.purple.value
