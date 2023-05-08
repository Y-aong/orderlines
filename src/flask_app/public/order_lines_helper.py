# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_helper.py
# Time       ：2023/3/12 14:20
# Author     ：blue_moon
# version    ：python 3.7
# Description：order lines 帮助类
"""

from ..order_lines_app.models.base_model import get_session
from ..order_lines_app.models.order_line_models import ProcessModel, TaskModel
from ..order_lines_app.schema.order_lines_schema import ProcessSchema, TaskSchema


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
