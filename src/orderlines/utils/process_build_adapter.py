# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_build_adapter.py
# Time       ：2023/7/26 22:57
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程适配器，可以从不同文件类中生成流程，例如json,yaml,dict, mysql
    Process adapter, which can generate processes from different file classes, such as json,yaml,dict
"""
import json
from abc import ABC, abstractmethod
from typing import List

import yaml

from apis.orderlines.models import Process, Task
from apis.orderlines.schema.process_schema import ProcessSchema
from apis.orderlines.schema.task_schema import TaskSchema
from public.base_model import get_session
from public.logger import logger


class BaseTarget(ABC):

    def __init__(self):
        self.process_orm = Process
        self.process_schema = ProcessSchema
        self.task_orm = Task
        self.task_schema = TaskSchema
        self.session = get_session()

    @abstractmethod
    def build_by_json(self, file_path: str):
        pass

    @abstractmethod
    def build_by_yaml(self, file_path: str):
        pass

    @abstractmethod
    def build_by_dict(self, process_info: dict, task_nodes: List[dict]):
        pass

    def build(self, process_info: dict, task_nodes: List[dict]):
        """
        创建流程和任务
        create process and task
        @param process_info:
        @param task_nodes:
        @return:
        """
        process_table_id, process_id = self._build_process(process_info)
        self._build_task(task_nodes, process_id)
        return process_table_id

    def _build_process(self, process_info: dict):
        """创建流程，create process"""
        data = dict()
        for key, val in process_info.items():
            if hasattr(self.process_orm, key):
                data.setdefault(key, val)
        process_info = self.process_schema().load(data)
        obj = self.process_orm(**process_info)
        self.session.add(obj)
        self.session.commit()
        return obj.id, obj.process_id

    def _build_task_node(self, node: dict, process_id: str):
        if node.get('process_id') and node.get('process_id') != process_id:
            raise ValueError('please check process node, process_id can not equal process info and task nodes')
        data = {'process_id': process_id}
        for key, val in node.items():
            if hasattr(self.task_orm, key):
                data.setdefault(key, val)

        task_node = self.task_schema().load(data)
        obj = self.task_orm(**task_node)
        self.session.add(obj)
        self.session.commit()

    def _build_task(self, task_nodes: List[dict], process_id):
        """创建任务节点, create task node"""
        for node in task_nodes:
            self._build_task_node(node, process_id)


class Adaptee:

    def __init__(self):
        self.session = get_session()
        self.task_types = ['common', 'process_control', 'parallel', 'group', 'start', 'end']

    def check_process_info(self, process_info):
        obj = self.session.query(Process).filter(Process.process_name == process_info.get('process_name')).first()
        if obj:
            raise ValueError(f'process name {process_info.get("process_name")} already exist')
        return process_info

    def check_task_nodes(self, task_nodes):
        for task_node in task_nodes:
            task_name = task_node.get('task_name')
            if task_node.get('task_type') not in self.task_types:
                raise ValueError(f'task type must in {self.task_types}')
            if not task_node.get('module version'):
                logger.warn(f'task name {task_name} has no module version')
        return task_nodes

    def adapter_json(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        process_info = self.check_process_info(content.get('process_info'))
        task_nodes = self.check_task_nodes(content.get('task_nodes'))
        return process_info, task_nodes

    def adapter_yaml(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = yaml.load(content, Loader=yaml.SafeLoader)
        process_info = self.check_process_info(content.get('process_info'))
        task_nodes = self.check_task_nodes(content.get('task_nodes'))
        return process_info, task_nodes

    def adapter_dict(self, process_info: dict, task_nodes: List[dict]):
        return self.check_process_info(process_info), self.check_task_nodes(task_nodes)


class ProcessBuildAdapter(BaseTarget):

    def __init__(self):
        super(ProcessBuildAdapter, self).__init__()
        self.adaptee = Adaptee()

    def build_by_json(self, file_path: str):
        process_info, task_nodes = self.adaptee.adapter_json(file_path)
        return self.build(process_info, task_nodes)

    def build_by_yaml(self, file_path):
        process_info, task_nodes = self.adaptee.adapter_yaml(file_path)
        return self.build(process_info, task_nodes)

    def build_by_dict(self, process_info: dict, task_nodes: List[dict]):
        process_info, task_nodes = self.adaptee.adapter_dict(process_info, task_nodes)
        return self.build(process_info, task_nodes)