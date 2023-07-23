# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : ProcessControl.py
# Time       ：2023/1/16 21:56
# Author     ：Y-aong
# version    ：python 3.7
# Description：流程控制
流程控制也是网关的一种，包括两种模式
模式1:对于流程返回值的判断走任务A还是任务B
模式2:对于流程的运行状态进行判断，成功——任务A，失败——任务B
"""
from typing import Any, Dict

from pydantic import Field, BaseModel

from conf.config import OrderLinesConfig
from order_lines.libraries.BaseTask import BaseTask
from order_lines.running.module_check import CheckModule
from order_lines.utils.base_orderlines_type import BasePluginParam
from public.language_type import get_desc_with_language


class ProcessControlType(BasePluginParam):
    conditions: Any = Field(description=get_desc_with_language('conditions'))
    expression: Dict = Field(description=get_desc_with_language('expression'))
    process_info: Dict = Field(description='流程信息')


class ProcessControlResult(BaseModel):
    task_id: str = Field(description=get_desc_with_language('task_id'))


class ProcessControl(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self):
        super(ProcessControl, self).__init__()
        self.condition = None
        self.expression = None
        self.modules = CheckModule().get_module()

    def process_control(self, process_control_type: ProcessControlType) -> ProcessControlResult:
        """
        process control is similar if elif else
        :param process_control_type:流程控制参数

        :return:
        """
        task_status = process_control_type.expression.get('success')
        if task_status:
            task_id = self._control_by_status(process_control_type.conditions,
                                              process_control_type.expression,
                                              process_control_type.process_info)
        else:
            task_id = self._control_by_condition(process_control_type.conditions, process_control_type.expression)
        return task_id

    def _get_module(self, node: dict):
        return self.modules.get(node.get('module_name'))

    @staticmethod
    def _get_task_status(task_id, process_instance_id):
        # 通过task_id和process_instance_id找到task_status
        from public.base_model import get_session
        from apis.order_lines.models import TaskInstanceModel
        session = get_session()
        task_status = session.query(TaskInstanceModel).filter(
            TaskInstanceModel.process_instance_id == process_instance_id,
            TaskInstanceModel.task_id == task_id
        ).first().task_status.lower()
        # 这里因为运行到这里，不可能出现pending和running
        return task_status if task_status in ['success', 'failure'] else 'failure'

    def _control_by_status(self, conditions, expression, process_info) -> int:
        """
        根据任务状态进行判断
        :param conditions:task_id如1001
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
        process_instance_id = process_info.get('process_instance_id')
        # 根据上一个节点的task_id获取到task_status
        task_status = self._get_task_status(conditions, process_instance_id)
        assert expression.get(task_status), f'根据此任务id::{conditions}找不到任务状态::{task_status}'
        self._get_module(expression.get(task_status))
        return expression.get(task_status).get('task_id')

    def _control_by_condition(self, conditions: list, expression: dict) -> int:
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
                    flag = self._parse_condition(item)
                    condition_filter.append(flag)
            if all(condition_filter) and expression.get(condition_name):
                self._get_module(expression.get(condition_name))
                return expression.get(condition_name).get('task_id')

        raise AttributeError('can not find condition')

    def _parse_condition(self, condition_data: ProcessControlType) -> bool:
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
