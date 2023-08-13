# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_control_strategy.py
# Time       ：2023/8/12 15:49
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程控制的变量处理方式
"""

from orderlines.variable.variable_strategy import BaseVariableStrategy


class ProcessControlVariableStrategy(BaseVariableStrategy):

    def handle_process_control_return_value(self, conditions: list):
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
               对于流程控制节点进行单独判断
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
               :return:
               """
        conditions = task_kwargs.get('conditions')
        if isinstance(conditions, str):
            return task_kwargs
        if isinstance(conditions, list):
            task_kwargs['conditions'] = self.handle_process_control_return_value(conditions)

        return task_kwargs
