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
from typing import List

from flask import Config

from order_lines.running.listen_running import ListenRunning
from order_lines.running.runner import TaskRunner
from public.base_model import get_session


class AppContent(object):
    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default):
        return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


class OrderLines:
    config_class = Config
    content = AppContent

    def __init__(self, process_info: dict, process_node: List[dict]):
        self.process_info = process_info
        self.process_node = process_node
        self.process_instance_id = str(uuid.uuid1().hex)
        self.process_name = process_info.get('process_name')
        self.process_info['process_instance_id'] = self.process_instance_id
        self.session = get_session()
        self.listen_running = ListenRunning(self.process_info)

    def start(self):
        t = TaskRunner(self.process_info, self.process_node, self.listen_running)
        t.start()

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

    def build_process(self):
        pass

    def logger(self):
        pass

    def make_config(self):
        pass
