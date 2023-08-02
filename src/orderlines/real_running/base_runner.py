# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_runner.py
# Time       ：2023/8/1 11:06
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines base runner
"""
from abc import ABC
from typing import List

from conf.config import OrderLinesConfig
from orderlines.real_running.app_context import AppContext
from public.logger import logger


class BaseRunner(ABC):
    def __init__(self, process_instance_id: str, context: AppContext):
        self.process_instance_id = process_instance_id
        self.context = context
        self.logger = logger

    @property
    def process_info(self) -> dict:
        return self.context.get_process_info(self.process_instance_id)

    @property
    def task_nodes(self) -> List[dict]:
        return self.context.get_task_nodes(self.process_instance_id)

    @property
    def process_name(self) -> str:
        return self.context.get_process_item(self.process_instance_id, 'process_name')

    @property
    def process_id(self) -> str:
        return self.context.get_process_item(self.process_instance_id, 'process_id')

    @property
    def process_config(self) -> dict:
        default_process_config = {
            "timeout": OrderLinesConfig.process_timeout,
        }
        return self.context.get_process_item(self.process_instance_id, 'process_config', default_process_config)

    def current_task_node(self, current_task_id: str) -> dict:
        return self.context.get_task_node(self.process_instance_id, current_task_id)

    def task_name(self, task_id: str) -> str:
        return self.context.get_task_node_item(self.process_instance_id, task_id, 'task_name')

    def task_kwargs(self, task_id: str) -> dict:
        return self.context.get_task_node_item(self.process_instance_id, task_id, 'method_kwargs', {})

    def task_config(self, task_id: str) -> dict:
        default_task_config = {
            'timeout': OrderLinesConfig.task_timeout,
            'task_strategy': OrderLinesConfig.task_strategy,
            'retry_time': OrderLinesConfig.retry_time,
            'notice_type': OrderLinesConfig.notice_type,
            'callback_func': OrderLinesConfig.callback_func,
            'callback_module': OrderLinesConfig.callback_module,
        }
        return self.context.get_task_node_item(self.process_instance_id, task_id, 'task_config', default_task_config)
