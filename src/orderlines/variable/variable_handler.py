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

# from orderlines.variable.common_task_strategy import CommonTaskVariableStrategy
# from orderlines.variable.process_control_strategy import ProcessControlVariableStrategy

from orderlines.variable.variable_strategy import BaseVariableStrategy


class ProcessControlVariableStrategy(BaseVariableStrategy):

    def handle_process_control_return_value(self, conditions: list):
        """
        handle process control params
        @param conditions:
        [
           {
               'A': [{'condition': 1, 'target': 1, 'sign': '='},
                     {'condition': 1, 'target': 3, 'sign': '>'}]
           },
           {
               'B': [{'condition': 2, 'target': "${add_value}", 'sign': '<'},
                     {'condition': 3, 'target': 3, 'sign': '='}]
           }
       ]
        @return:
        """
        for _condition in conditions:
            for _, single_condition in _condition.items():
                for temp in single_condition:
                    condition = temp.get('condition')
                    target = temp.get('target')
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
            {
            "conditions": [
                {
                    'A': [{'condition': 1, 'target': 1, 'sign': '='},
                          {'condition': 1, 'target': 3, 'sign': '>'}]
                },
                {
                    'B': [{'condition': 2, 'target': "${add_value}", 'sign': '<'},
                          {'condition': 3, 'target': 3, 'sign': '='}]
                }
            ],
            "expression": {
                'A': {'task_id': 1014},
                'B': {'task_id': 1015}
            },
        }
           :return:
        """
        conditions = task_kwargs.get('conditions')
        if isinstance(conditions, str):
            return task_kwargs
        if isinstance(conditions, list):
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
