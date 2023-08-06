# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : app_context.py
# Time       ：2023/7/31 21:45
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines app context
"""


class AppContext(object):
    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default):
        return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def get_process_info(self, process_instance_id: str, default=None) -> dict:
        process_instance_info = self.get(process_instance_id, {})
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

    def get_task_nodes(self, process_instance_id):
        process_instance_info = self.__dict__.get(process_instance_id, {})
        return process_instance_info.get('task_nodes', {})

    def get_task_node(self, process_instance_id: str, task_id: str, default=None) -> dict:
        """获取当前正在运行的任务节点"""
        process_instance_info = self.__dict__.get(process_instance_id, {})
        task_nodes = process_instance_info.get('task_nodes', {})
        for task_node in task_nodes:
            if task_node.get('task_id') == task_id:
                return task_node
        return default

    def get_task_node_item(
            self,
            process_instance_id: str,
            task_id: str,
            item_name: str,
            default=None
    ):
        task_node = self.get_task_node(process_instance_id, task_id)
        item = task_node.get(item_name)
        return item if item else default

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
