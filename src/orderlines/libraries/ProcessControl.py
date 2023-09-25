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
from orderlines.task_running.running_check import CheckModule
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
        流程控制
        控制流程的运行节点
        Control the running nodes of the flow
        :param process_control_type:process control param type
        :return:
        """

        if process_control_type.pc_type == 'status':
            task_id = self._control_by_status(
                process_control_type.conditions,
                process_control_type.process_info
            )
        else:
            task_id = self._control_by_condition(process_control_type.conditions)
        return task_id

    def _get_module(self, node: dict):
        return self.modules.get(node.get('module_name'))

    @staticmethod
    def _get_task_status(task_id: str, process_instance_id: str) -> str:
        from public.base_model import get_session
        from apis.orderlines.models import TaskInstance
        from apis.orderlines.schema.task_schema import TaskInstanceSchema

        session = get_session()
        obj = session.query(TaskInstance).filter(
            TaskInstance.process_instance_id == process_instance_id,
            TaskInstance.task_id == task_id
        ).first()
        task_instance_info = TaskInstanceSchema().dump(obj)
        task_status = task_instance_info.get('task_status')
        # 这里因为运行到这里，不可能出现pending和running
        # pending and running are not possible here because we're running here
        return task_status if task_status in ['success', 'failure'] else 'failure'

    def _control_by_status(self, conditions, process_info) -> str:
        """
        根据任务状态进行判断
        Determine the task status
        :param conditions
        [
            {
                'task_id': '1014',
                'condition': [{'task_status': 'success', 'condition_task_id': '1012'}]
            },
            {
                'task_id': '1015',
                'condition': [{'task_status': 'failure', 'condition_task_id': '1012'}]
            }
        ]
        :return: task_id
        """
        condition_task_id = None
        process_instance_id = process_info.get('process_instance_id')
        # 根据上一个节点的task_id获取到task_status
        # The task status is obtained based on the task id of the previous node
        for item in conditions:
            condition_flags = list()
            task_id = item.task_id
            condition = item.condition
            for temp in condition:
                task_status_config = temp.get('task_status')
                condition_task_id = temp.get('condition_task_id')

                task_status = self._get_task_status(condition_task_id, process_instance_id)
                assert task_status, f'task id::{condition_task_id} can not find task status ::{task_status}'
                condition_flags.append(task_status_config == task_status)
            if all(condition_flags):
                return task_id
        raise ValueError(f'can not find condition by {condition_task_id}')

    def _control_by_condition(self, conditions: list) -> str:
        """
        根据任务的返回值进行判断
        Make a judgment based on the return value of the task
        :param conditions:list
        [
            {
                'task_id': '1014',
                'condition': [
                    {'sign': '=', 'target': 788, 'condition': 1},
                    {'sign': '>', 'target': 3, 'condition': 1}
                ]
            },
            {
                'task_id': '1015',
                'condition': [
                    {'sign': '<', 'target': 788, 'condition': 2},
                    {'sign': '=', 'target': 3, 'condition': 3}
                ]
            }
        ]

        :return: task_id
        """
        for item in conditions:
            condition_flags = list()
            task_id = item.task_id
            condition = item.condition
            for temp in condition:
                flag = self._parse_condition(temp)
                condition_flags.append(flag)
            if all(condition_flags):
                return task_id

        raise AttributeError('can not find condition.')

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
