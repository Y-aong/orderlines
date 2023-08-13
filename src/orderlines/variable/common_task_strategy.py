# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : common_task_strategy.py
# Time       ：2023/8/12 15:05
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    普通方法变量解析
"""
from orderlines.variable.variable_strategy import BaseVariableStrategy


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
