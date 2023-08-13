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

from orderlines.variable.common_task_strategy import CommonTaskVariableStrategy
from orderlines.variable.process_control_strategy import ProcessControlVariableStrategy


class VariableHandlerReal:
    def __init__(self, process_instance_id: str, ):
        self.process_instance_id = process_instance_id
        self.variable_handles = {
            'common': CommonTaskVariableStrategy(process_instance_id),
            'process_control': ProcessControlVariableStrategy(process_instance_id),
        }

    def variable_handle_params(self, task_type: str, task_kwargs: dict) -> dict:
        """
        任务参数变量处理
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
        任务返回值变量处理
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
