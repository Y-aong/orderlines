# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_helper.py
# Time       ：2023/3/12 14:20
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines 帮助类
    orderlines helper class
"""
from apis.order_lines.models import TaskModel
from apis.order_lines.models.process import ProcessModel
from apis.order_lines.schema.process_schema import ProcessSchema
from apis.order_lines.schema.task_schema import TaskSchema
from public.base_model import get_session


class OrderLinesHelper:
    def __init__(self, process_id: str):
        self.process_id = process_id
        self.session = get_session()

    def get_process_info(self):
        process_info = self.session.query(ProcessModel).filter(ProcessModel.process_id == self.process_id).first()
        process_info = ProcessSchema().dump(process_info)
        if process_info.get('id'):
            process_info.pop('id')
        return process_info

    def get_process_node(self):
        tasks_info = self.session.query(TaskModel).filter(TaskModel.process_id == self.process_id).all()
        process_node = TaskSchema().dump(tasks_info, many=True)
        for node in process_node:
            if node.get('id'):
                node.pop('id')
        return process_node

    def get_process(self):
        process = dict()
        process['process_info'] = self.get_process_info()
        process['process_node'] = self.get_process_node()
        return process
