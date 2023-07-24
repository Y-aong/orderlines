# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_handler.py
# Time       ：2023/2/22 22:46
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    变量运算, 目前支持int四则运算，和str拼接
    Variable operation, currently support int four operations, and str concatenation
"""
from typing import List
from copy import deepcopy
from order_lines.operators.variable import VariableModelOperator
from public.logger import logger
from order_lines.utils.utils import get_variable_value
from order_lines.variable.match import Match
from order_lines.variable.variable_operator import VariableOperator


class VariableHandler:

    def __init__(self, task_id: str, task_name: str, process_info: dict):
        self.task_id = task_id
        self.task_name = task_name
        self.process_info = process_info
        self.process_id = process_info.get('process_id')
        self.process_instance_id = process_info.get('process_instance_id')
        self.process_name = process_info.get('process_name')

    def handle_param_with_variable(self, params_value):
        """
        获取流程中的带有变量的参数
        Gets parameters with variables in the process
        :param params_value:param value
        :return:
        """
        variable_name = Match(params_value).get_variable_name()
        variable = VariableModelOperator(self.task_id, variable_name)
        variable_instance = variable.select_data(self.process_instance_id, variable_name)
        real_variable_value = variable_instance.variable_value if variable_instance else None
        variable_type = variable_instance.variable_type
        real_variable_value = VariableOperator(variable_name, real_variable_value, variable_type).variable_operator()
        return get_variable_value(real_variable_value, variable_type)

    def handle_process_control_return_value(self, conditions: list):
        for _condition in conditions:
            for _, single_condition in _condition.items():
                for temp in single_condition:
                    condition = temp.get('condition')
                    target = temp.get('target')
                    if isinstance(condition, str) and '${' in condition and '}' in condition:
                        condition_value = self.handle_param_with_variable(condition)
                        temp['condition'] = condition_value
                    if isinstance(target, str) and '${' in target and '}' in target:
                        target_value = self.handle_param_with_variable(target)
                        temp['target'] = target_value
        return conditions

    def handle_process_control_params(self, node_params: dict):
        """
        对于流程控制节点进行单独判断
        Process control nodes are judged individually
        :param node_params:
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
        conditions = node_params.get('conditions')
        if isinstance(conditions, str):
            return node_params
        if isinstance(conditions, list):
            node_params['conditions'] = self.handle_process_control_return_value(conditions)

        return node_params

    def handle_common_node(self, node_params):
        for params_key, params_value in node_params.items():
            if isinstance(params_value, str) and '${' in params_value and '}' in params_value:
                # 参数中存在变量,处理
                variable_value = self.handle_param_with_variable(params_value)
                node_params[params_key] = variable_value
        return node_params

    def handle_node_params(self, node_params: dict, task_type):
        """
        解析流程中的参数
        Parse the parameters in the process
        :param node_params: { "a": "${add_value}", "b": 2}
        :param task_type: task type
        :return:
        """
        # 普通流程判断流程中的参数是否存在变量
        # Common node whether parameters in the process have variables
        if not node_params:
            return {}
        if task_type == 'process_control':
            return self.handle_process_control_params(node_params)
        else:
            return self.handle_common_node(node_params)

    def handle_node_return(self, node_results: List[dict], task_result: dict):
        """
        处理任务返回值的
        Process task return value
        :param node_results: 流程的返回值参数,The return value parameter of the process
        :param task_result: 任务的返回值,The return value of the task
        :return:task_result
        """
        if not node_results:
            return task_result
        for node_result in node_results:
            _node_result = deepcopy(node_result)
            for node_variable_key, node_variable_value in _node_result.items():
                task_variable_value = task_result.get(node_variable_key)
                real_variable_value = self._update_variable_value(task_variable_value, node_result, node_variable_value)
                # 对于task_result重新赋值
                if task_result.get(node_variable_key):
                    task_result[node_variable_key] = real_variable_value
        return task_result

    def _update_variable_value(self, task_variable_value, node_result, node_variable_value):
        """
        update variable_value
        :param task_variable_value:真正的数据值,Real data values
        :param node_result: 变量的信息,Variable information
        :param node_variable_value: 节点中变量配置的值,The value of the variable configuration in the node
        :return:
        """
        if task_variable_value:
            variable_name = Match(node_variable_value).get_variable_name()
            variable = VariableModelOperator(self.task_id, variable_name)
            variable_instance = variable.select_data(self.process_instance_id, variable_name)
            variable_type = node_result.get('variable_type')
            variable_operator = VariableOperator(node_variable_value, task_variable_value, variable_type)
            real_variable_value = variable_operator.variable_operator()
            if variable_instance:
                logger.info(f'variable {variable_name, real_variable_value, node_result} update db success')
                node_result.setdefault('variable_name', variable_name)
                variable.update_db(self.process_instance_id, self.task_name, real_variable_value, **node_result)
            else:
                logger.info(f'variable {variable_name, real_variable_value, node_result} add db success')
                variable.insert_db(self.process_info, real_variable_value, node_result, self.task_name)

            return real_variable_value
