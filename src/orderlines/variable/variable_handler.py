# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_handler.py
# Time       ：2023/8/12 16:26
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    变量处理统一入口
"""
from typing import List

from orderlines.variable.variable_strategy import BaseVariableStrategy


class ProcessControlVariableStrategy(BaseVariableStrategy):

    def handle_process_control_return_value(self, conditions: list):
        """
        handle process control params
        @param conditions:
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
        @return:
        """
        for item in conditions:
            temp = item.get('condition')
            for condition_item in temp:
                condition = condition_item.get('condition')
                target = condition_item.get('target')
                if isinstance(condition, str) and '${' in condition and '}' in condition:
                    condition_value = self._handle_param_with_variable(condition)
                    temp['condition'] = condition_value
                if isinstance(target, str) and '${' in target and '}' in target:
                    target_value = self._handle_param_with_variable(target)
                    temp['target'] = target_value
        return conditions

    def handle_task_kwargs(self, task_kwargs: dict) -> dict:
        """
           对于流程控制节点进行单独判断,Process control nodes are judged individually
           Process control nodes are judged individually
           :param task_kwargs:
            pc_type = 'result',
            conditions = [
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
           :return:
        """
        pc_type = task_kwargs.get('pc_type')
        conditions = task_kwargs.get('conditions')
        if pc_type == 'result':
            task_kwargs['conditions'] = self.handle_process_control_return_value(conditions)
        return task_kwargs


class CommonTaskVariableStrategy(BaseVariableStrategy):

    def __init__(self, process_instance_id: str):
        super(CommonTaskVariableStrategy, self).__init__(process_instance_id)

    def handle_task_kwargs(self, task_kwargs: dict) -> dict:
        """
        获取任务节点中带有变量的任务参数
        @param task_kwargs: 任务参数
         "method_kwargs": {
            "a": "${add_value}",
            "b": 123123
        },
        @return: 返回解析后的的任务参数
        """
        parsed_task_kwargs = dict()
        if not task_kwargs:
            return parsed_task_kwargs

        for variable_key, variable_value in task_kwargs.items():
            if isinstance(variable_value, str) and '${' in variable_value and '}' in variable_value:
                variable_value = self._handle_param_with_variable(variable_value)
                parsed_task_kwargs[variable_key] = variable_value
            else:
                parsed_task_kwargs.setdefault(variable_key, variable_value)
        return parsed_task_kwargs


class VariableHandlerReal:
    def __init__(self, process_instance_id: str, ):
        self.process_instance_id = process_instance_id
        self.variable_handles = {
            'common': CommonTaskVariableStrategy(process_instance_id),
            'process_control': ProcessControlVariableStrategy(process_instance_id),
        }

    def variable_handle_params(self, task_type: str, task_kwargs: dict) -> dict:
        """
        任务参数变量处理,Task parameter variable processing
        @param task_type: 任务类型
        @param task_kwargs: 任务参数
        @return:
        """
        variable_handler = self.variable_handles.get(task_type)
        if not variable_handler:
            return task_kwargs

        return variable_handler.handle_task_kwargs(task_kwargs)

    def variable_handle_result(
            self,
            task_type: str,
            variable_config: List[dict],
            task_result: dict,
            node_result_config: dict
    ) -> dict:
        """
        任务返回值变量处理,Task return value variable processing
        @param task_type: 任务类型
        @param variable_config: 变量配置
        @param task_result: 任务返回值
        @param node_result_config: 任务节点中配置的返回值
        @return:
        """
        variable_handler = self.variable_handles.get(task_type)
        if not variable_handler:
            return task_result

        return variable_handler.handle_task_result(variable_config, task_result, node_result_config)
