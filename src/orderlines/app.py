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

from apis.orderlines.models import Process, Variable, VariableInstance
from apis.orderlines.schema.process_schema import ProcessRunningSchema
from conf.config import OrderLinesConfig
from orderlines.task_running.app_context import AppContext
from orderlines.task_running.task_runner import TaskRunner

from orderlines.utils.process_build_adapter import ProcessBuildAdapter
from public.base_model import get_session
from public.logger import logger


class OrderLines:
    config_class = Config

    def __init__(self):
        self.session = get_session()
        self.process_build = ProcessBuildAdapter()
        self.context = AppContext()
        self.logger = logger

    def clear_db(self):
        from apis.orderlines.models import Process, ProcessInstance, Task, TaskInstance

        self.session.query(TaskInstance).delete()
        self.session.commit()

        self.session.query(Task).delete()
        self.session.commit()

        self.session.query(ProcessInstance).delete()
        self.session.commit()

        self.session.query(Process).delete()
        self.session.commit()

        self.session.query(Variable).delete()
        self.session.commit()

        self.session.query(VariableInstance).delete()
        self.session.commit()

    def start_by_process_id(self, process_id: Union[int, str], dry):
        if isinstance(process_id, str):
            obj = self.session.query(Process).filter(Process.process_id == process_id).first()
        elif isinstance(process_id, int):
            obj = self.session.query(Process).filter(Process.id == process_id).first()
        else:
            raise ValueError(f'process id {process_id} type is not support. process id is only support int or str')
        process_info = ProcessRunningSchema().dump(obj)
        task_nodes = process_info.pop('task')
        self._start(process_info, task_nodes, dry)

    def start_by_file_path(self, file_path: str, dry):
        if file_path.endswith('json'):
            process_id = self.process_build.build_by_json(file_path)
        elif file_path.endswith('yaml'):
            process_id = self.process_build.build_by_yaml(file_path)
        else:
            raise ValueError('file type is not support. orderlines is only support json or yaml')
        self.start_by_process_id(process_id, dry)

    def start_by_dict(self, process_info: dict, task_nodes: List[dict], variable: List[dict], dry):
        process_id = self.process_build.build_by_dict(process_info, task_nodes, variable)
        self.start_by_process_id(process_id, dry)

    @property
    def default_task_config(self):
        task_config = dict()
        task_config.setdefault('timeout', OrderLinesConfig.task_timeout)
        task_config.setdefault('task_strategy', OrderLinesConfig.task_strategy)
        task_config.setdefault('retry_time', OrderLinesConfig.retry_time)
        task_config.setdefault('notice_type', OrderLinesConfig.notice_type)
        task_config.setdefault('callback_func', OrderLinesConfig.callback_func)
        task_config.setdefault('callback_module', OrderLinesConfig.callback_module)
        return task_config

    def _start(self, process_info: dict, task_nodes: List[dict], dry):
        process_instance_id = str(uuid.uuid1().hex)
        process_info['process_instance_id'] = process_instance_id
        for task_node in task_nodes:
            if not task_node.get('method_kwargs'):
                task_node['method_kwargs'] = {}
            task_node['task_config'] = self.default_task_config
        process_instance_info = {'process_info': process_info, 'task_nodes': task_nodes}
        self.context.setdefault(process_instance_id, process_instance_info)
        t = TaskRunner(process_instance_id, self.context, dry)
        t.start()

    def start(
            self,
            process_id: Union[None, int, str] = None,
            file_path: str = None,
            process_info: dict = None,
            task_nodes: List[dict] = None,
            variable: List[dict] = None,
            dry: bool = False
    ) -> None:
        """
        启动流程
        start process
        @param process_id: process_id or process table id
        @param file_path: start by file ,now only support json or yaml
        @param process_info: process info base process table info
        @param task_nodes: task node one process can have many task node
        @param variable: process variable
        @param dry: True——not insert into db, False——insert into db
        @return:
        """
        if process_id:
            self.start_by_process_id(process_id, dry)
        elif file_path:
            self.start_by_file_path(file_path, dry)
        else:
            self.start_by_dict(process_info, task_nodes, variable, dry)

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

    def make_config(self):
        pass
