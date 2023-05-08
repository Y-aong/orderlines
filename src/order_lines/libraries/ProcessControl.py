# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : ProcessControl.py
# Time       ：2023/1/16 21:56
# Author     ：blue_moon
# version    ：python 3.7
# Description：流程控制
流程控制也是网关的一种，包括两种模式
模式1:对于流程返回值的判断走任务A还是任务B
模式2:对于流程的运行状态进行判断，成功——任务A，失败——任务B
"""
from typing import Any

from order_lines.libraries.BaseTask import BaseTask, run_keyword_variant
from order_lines.running.module_check import CheckModule


class ProcessControl(BaseTask):
    def __init__(self):
        super(ProcessControl, self).__init__()
        self.condition = None
        self.expression = None
        self.modules = CheckModule().get_module()

    @run_keyword_variant('ProcessControl')
    def process_control(self, conditions: Any, expression: dict, **kwargs) -> int:
        """
        process control is similar if elif else
        :param conditions:条件
        :param expression:条件表达式
        :return:
        """
        task_status = expression.get('success')
        if task_status:
            task_id = self.control_by_status(conditions, expression)
        else:
            task_id = self.control_by_condition(conditions, expression)
        return task_id

    def get_module(self, node: dict):
        return self.modules.get(node.get('module_name'))

    def control_by_status(self, conditions, expression) -> int:
        """
        根据任务状态进行判断
        :param conditions:str success/failure
        :param expression:{
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

        assert expression.get(conditions), 'please check conditions'
        self.get_module(expression.get(conditions))
        return expression.get(conditions).get('task_id')

    def control_by_condition(self, conditions: list, expression: dict) -> int:
        """
        根据任务的返回值进行判断
        :param conditions:list [
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

        :param expression:{
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
                    flag = self.parse_condition(item)
                    condition_filter.append(flag)
            if all(condition_filter) and expression.get(condition_name):
                self.get_module(expression.get(condition_name))
                return expression.get(condition_name).get('task_id')

        raise AttributeError('can not find condition')

    def parse_condition(self, condition_data: dict) -> bool:
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
