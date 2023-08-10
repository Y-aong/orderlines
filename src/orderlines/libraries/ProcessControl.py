# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : ProcessControl.py
# Time       ：2023/1/16 21:56
# Author     ：Y-aong
# version    ：python 3.7
# Description：流程控制, Process control
流程控制

流程控制也是网关的一种，包括两种模式
模式1:对于流程返回值的判断走任务A还是任务B
模式2:对于流程的运行状态进行判断，成功——任务A，失败——任务B

Process control

process control is also a kind of gateway, including two modes
Mode 1: The process return value is determined by task A or Task B
Mode 2: Judging the running state of the process, success - Task A, failure - Task B
"""

from conf.config import OrderLinesConfig
from orderlines.libraries.BaseTask import BaseTask
from orderlines.running.module_check import CheckModule
from orderlines.utils.base_orderlines_type import ProcessControlParam, ProcessControlResult


class ProcessControl(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self):
        super(ProcessControl, self).__init__()
        self.condition = None
        self.expression = None
        self.modules = CheckModule().get_module()

    def process_control(self, process_control_type: ProcessControlParam) -> ProcessControlResult:
        """
        流程控制，控制流程的运行节点
        Control the running nodes of the flow
        :param process_control_type:process control param type
        :return:
        """
        task_status = process_control_type.expression.get('success')
        if task_status:
            task_id = self._control_by_status(
                process_control_type.conditions,
                process_control_type.expression,
                process_control_type.process_info
            )
        else:
            task_id = self._control_by_condition(process_control_type.conditions, process_control_type.expression)
        return task_id

    def _get_module(self, node: dict):
        return self.modules.get(node.get('module_name'))

    @staticmethod
    def _get_task_status(task_id: str, process_instance_id: str) -> str:
        from public.base_model import get_session
        from apis.orderlines.models import TaskInstance
        session = get_session()
        task_status = session.query(TaskInstance).filter(
            TaskInstance.process_instance_id == process_instance_id,
            TaskInstance.task_id == task_id
        ).first().task_status.lower()
        # 这里因为运行到这里，不可能出现pending和running
        # pending and running are not possible here because we're running here
        return task_status if task_status in ['success', 'failure'] else 'failure'

    def _control_by_status(self, conditions, expression, process_info) -> str:
        """
        根据任务状态进行判断
        Determine the task status
        :param conditions:task_id如1001
        :param expression:
        {
        'success': {
            'task_id':'2',
            'method_name': 'add',
            'method_kwargs': {"x": 10,"y": 2},
            'module': 'TestAdd'},
        'failure': {
            'task_id':'1',
            'method_name': 'subtraction',
            'method_kwargs': {"x": 10,"y": 2},
            'module': 'TestSubtraction'}
        }
        :return: task_id
        """
        process_instance_id = process_info.get('process_instance_id')
        # 根据上一个节点的task_id获取到task_status
        # The task status is obtained based on the task id of the previous node
        task_status = self._get_task_status(conditions, process_instance_id)
        assert expression.get(task_status), f'user task id::{conditions} can not find task status ::{task_status}'
        self._get_module(expression.get(task_status))
        return expression.get(task_status).get('task_id')

    def _control_by_condition(self, conditions: list, expression: dict) -> str:
        """
        根据任务的返回值进行判断
        Make a judgment based on the return value of the task
        :param conditions:list
        [
            {
                'A': [{'condition': 1, 'target': 1, 'sign': '='},
                    {'condition': 1, 'target': 3, 'sign': '>'}]
            },
            {
                'B': [{'condition': 2, 'target': 3, 'sign': '<'},
                    {'condition': 3, 'target': 3, 'sign': '='}]
            },
            {'C': [{'condition': 2, 'target': 3, 'sign': '<'}]}
        ]
        :param expression:dict
        {
        'A': {
            'task_id':'1',
            'method_name': 'add',
            'method_kwargs': {"x": 10, "y": 2},
            'module': 'TestAdd'},
        'B': {
            'task_id':'2',
            'method_name': 'subtraction',
            'method_kwargs': {"x": 10, "y": 2},
            'module': 'TestSubtraction'},
        'C': {
            'task_id':'3',
            'method_name': 'subtraction',
            'method_kwargs': {"x": 10, "y": 2},
            'module': 'TestSubtraction'}
        }
        :return: task_id
        """
        for temps in conditions:
            condition_filter = list()
            condition_name = list(temps.keys()).pop()
            for temp in list(temps.values()):
                for item in temp:
                    flag = self._parse_condition(item)
                    condition_filter.append(flag)
            if all(condition_filter) and expression.get(condition_name):
                self._get_module(expression.get(condition_name))
                return expression.get(condition_name).get('task_id')

        raise AttributeError('can not find condition')

    def _parse_condition(self, condition_data: ProcessControlParam) -> bool:
        """解析条件"""
        target = condition_data.get('target')
        self.condition = condition_data.get('condition')
        sign = condition_data.get('sign')
        sign_handler = {
            '=': self.__eq__(target),
            '>': self.__gt__(target),
            '>=': self.__ge__(target),
            '<=': self.__le__(target),
            '<': self.__lt__(target)
        }
        return sign_handler.get(sign)

    def __eq__(self, other):
        if not type(self.condition) == type(other):
            return False
        return self.condition == other

    def __gt__(self, other):
        if not type(self.condition) == type(other):
            return False
        return self.condition > other

    def __ge__(self, other):
        if not type(self.condition) == type(other):
            return False
        return self.condition >= other

    def __le__(self, other):
        if not type(self.condition) == type(other):
            return False
        return self.condition <= other

    def __lt__(self, other):
        if not type(self.condition) == type(other):
            return False
        return self.condition < other


# task_config = {
#     'timeout': 120,
#     'task_strategy': 'RAISE',
#     'retry_time': 3,
#     'notice_type': 'FAILURE',
#     'callback_func': 'send_msg',
#     'callback_module': 'Email'
# }
# conditions = [
#     {'A': [{'sign': '=', 'target': '${add_value}', 'condition': 1}, {'sign': '>', 'target': 3, 'condition': 1}]},
#     {'B': [{'sign': '<', 'target': '${add_value}', 'condition': 2}, {'sign': '=', 'target': 3, 'condition': 3}]}
# ]
# expression = {'A': {'task_id': '1014'}, 'B': {'task_id': '1015'}}
# process_info = {
#     'process_config': None,
#     'creator': 'blue',
#     'process_id': '1007',
#     'desc': None,
#     'process_params': None,
#     'process_name': 'test_process_return',
#     'updater': None,
#     'process_instance_id': 'ff54c4fb378e11eebef7001a7dda7111'
# }
# data = {
#     'task_config': task_config,
#     'conditions': conditions,
#     'expression': expression,
#     'process_info': process_info,
# }
# ProcessControl().process_control(
#     ProcessControlParam(**data)
# )
