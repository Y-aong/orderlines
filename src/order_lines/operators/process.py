# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process.py
# Time       ：2023/1/10 22:41
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务流程操作api
    process instance operator
"""
import json

from apis.order_lines.models.process import ProcessInstance
from order_lines.utils.process_action_enum import ProcessStatus


class ProcessInstanceOperator:

    def __init__(self, process_data: dict):
        self.process_data = process_data
        self.process_id = self.process_data.get('process_id')
        self.process_instance_id = self.process_data.get('process_instance_id')
        self.process_params = json.dumps(self.process_data.get('process_params'))
        self.process_config = json.dumps(self.process_data.get('process_config'))

    def insert_db(self):
        process_info = dict()
        process_info.update(self.process_data)
        process_info['process_params'] = self.process_params
        process_info['process_config'] = self.process_config
        process_info['process_instance_id'] = self.process_instance_id
        process_info['process_id'] = self.process_id
        process_info['runner'] = self.process_data.get('creator')
        process_info['process_status'] = ProcessStatus.grey.value
        print(f'process_info::{process_info}')
        return ProcessInstance.insert_db(ProcessInstance, process_info)

    @staticmethod
    def update_db(process_instance_id: str, **kwargs) -> int:
        """
        修改变量信息，变量名一旦创建不能修改
        Modify variable information. A created variable name cannot be modified
        """
        filter_data = {'process_instance_id': process_instance_id}
        return ProcessInstance.update_db(ProcessInstance, filter_data, kwargs)

    @staticmethod
    def select_data(process_instance_id=None):
        """
        获取流程中的变量数据
        Get variable data in the process
        """
        filter_data = {'process_instance_id': process_instance_id}
        return ProcessInstance.select_db(ProcessInstance, filter_data)
