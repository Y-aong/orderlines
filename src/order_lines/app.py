# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : app.py
# Time       ：2023/3/7 21:04
# Author     ：Y-aong
# version    ：python 3.7
# Description：orderlines app
"""

import uuid
from typing import List, Union

from flask import Config

from apis.order_lines.models import Process
from apis.order_lines.schema.process_schema import ProcessRunningSchema
from order_lines.running.listen_running import ListenRunning
from order_lines.running.runner import TaskRunner
from order_lines.utils.process_build_adapter import ProcessBuildAdapter
from public.base_model import get_session


class AppContent(object):
    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default):
        return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def get_process_info(self, process_instance_id: str, default=None) -> dict:
        process_instance_info = self.get_process_info(process_instance_id, {})
        return process_instance_info.get('process_info', default)

    def get_process_item(self, process_instance_id: str, item_name: str, default=None):
        process_info = self.get_process_info(process_instance_id)
        return process_info.get(item_name) if process_info else default

    def get_process_items(self, process_instance_id: str, *args) -> dict:
        process_items = dict()
        process_info = self.get_process_info(process_instance_id)
        for item_name in args:
            item = process_info.get(item_name, None)
            if process_info and item:
                process_items.setdefault(item_name, item)
        return process_items

    def get_task_node(self, process_instance_id: str, task_id: str, default=None) -> dict:
        """获取当前正在运行的任务节点"""
        process_instance_info = self.__dict__.get(process_instance_id, {})
        task_nodes = process_instance_info.get('task_nodes', {})
        for task_node in task_nodes:
            if task_node.get('task_id') == task_id:
                return task_node
        return default

    def get_task_node_item(self, process_instance_id: str, task_id: str, item_name: str, default=None):
        task_node = self.get_task_node(process_instance_id, task_id)
        return default if not task_node else task_node.get(item_name)

    def get_task_node_items(self, process_instance_id: str, task_id: str, *args):
        task_node = self.get_task_node(process_instance_id, task_id)
        node_items = dict()
        for item_name in args:
            if task_node and task_node.get(item_name):
                node_items.setdefault(item_name, task_node.get(item_name))
        return node_items

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


class OrderLines:
    config_class = Config

    def __init__(self, process_info: dict, process_node: List[dict]):
        self.process_info = process_info
        self.process_node = process_node
        # self.process_instance_id = str(uuid.uuid1().hex)
        self.process_name = process_info.get('process_name')
        self.process_info['process_instance_id'] = self.process_instance_id
        self.session = get_session()
        self.process_build = ProcessBuildAdapter()
        self.content = AppContent()

    @property
    def process_instance_id(self):
        return str(uuid.uuid1().hex)

    def start_by_process_id(self, process_id: Union[int, str]):
        if isinstance(process_id, str):
            obj = self.session.query(Process).filter(Process.process_id == process_id).first()
        elif isinstance(process_id, int):
            obj = self.session.query(Process).filter(Process.id == process_id).first()
        else:
            raise ValueError(f'process id {process_id} type is not legal. process is only support int or str')
        process_info = ProcessRunningSchema().dump(obj)
        task_nodes = process_info.pop('task_nodes')
        self._start(process_info, task_nodes)

    def start_by_file_path(self, file_path: str):
        if file_path.endswith('json'):
            process_id = self.process_build.build_by_json(file_path)
        elif file_path.endswith('yaml'):
            process_id = self.process_build.build_by_yaml(file_path)
        else:
            raise ValueError('file type is not support. orderlines is only support json or yaml')
        self.start_by_process_id(process_id)

    def _start(self, process_info: dict, task_nodes: List[dict]):
        self.process_info['process_instance_id'] = self.process_instance_id
        process_instance_info = {'process_info': process_info, 'task_nodes': task_nodes}
        self.content.setdefault(self.process_instance_id, process_instance_info)
        TaskRunner(process_info, task_nodes,
                   ListenRunning(self.process_instance_id, self.process_info.get('process_id')))

    def start(self,
              process_id: Union[None, int, str] = None,
              file_path: str = None,
              process_info: dict = None,
              task_nodes: List[dict] = None):
        """
        启动流程
        start process
        @param process_id: process_id or process table id
        @param file_path: start by file ,now only support json or yaml
        @param process_info: process info base process table info
        @param task_nodes: task node one process can have many task node
        @return:
        """
        if process_info:
            self.start_by_process_id(process_id)
        elif file_path:
            self.start_by_process_id(file_path)
        else:
            self._start(process_info, task_nodes)

    def stop_process(self, process_instance_id: str):
        pass

    def stop_all(self):
        pass

    def paused_process(self, process_instance_id: str):
        pass

    def paused_all(self):
        pass

    def continue_process(self, process_instance_id: str):
        pass

    def continue_all(self):
        pass

    def logger(self):
        pass

    def make_config(self):
        pass
