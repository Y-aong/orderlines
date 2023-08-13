# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_strategy.py
# Time       ：2023/8/12 14:41
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务变量处理策略
    task variable handle strategy
"""
import copy
from abc import ABC, abstractmethod
from typing import Any, List

from apis.orderlines.models import ProcessInstance
from apis.orderlines.models.variable import VariableInstance
from apis.orderlines.schema.process_schema import ProcessInstanceSchema
from apis.orderlines.schema.variable_schema import VariableInfoSchema
from orderlines.utils.exceptions import VariableException
from orderlines.variable.variable_match import VariableMatch
from orderlines.variable.variable_operator import VariableOperator
from public.base_model import get_session
from public.logger import logger


class BaseVariableStrategy(ABC):

    def __init__(self, process_instance_id: str):
        self.process_instance_id = process_instance_id
        self.session = get_session()

    def _handle_param_with_variable(self, variable_config_value: str):
        variable_name = VariableMatch(variable_config_value).get_variable_name()
        variable_info = self.get_variable(self.process_instance_id, variable_name)
        real_variable_value = variable_info.get('variable_value')
        variable_type = variable_info.get('variable_type')
        variable_operator = VariableOperator(variable_config_value, real_variable_value, variable_type)
        variable_value = variable_operator.variable_operator()
        return variable_value

    def variable_insert(self, process_instance_id: str, variable_info: dict) -> None:
        obj = self.session.query(ProcessInstance).filter(
            ProcessInstance.process_instance_id == process_instance_id).first()
        process_instance = ProcessInstanceSchema().dump(obj)
        obj = self.session.query(VariableInstance).filter(
            VariableInstance.process_instance_id == self.process_instance_id,
            VariableInstance.variable_key == variable_info.get('variable_key')
        ).first()
        process_instance_info = {
            'process_instance_id': process_instance_id,
            'process_id': process_instance.get('process_id'),
            'process_name': process_instance.get('process_name')
        }
        variable_info.update(process_instance_info)
        if obj:
            self.session.query(VariableInstance).filter(
                VariableInstance.process_instance_id == self.process_instance_id,
                VariableInstance.variable_key == variable_info.get('variable_key')
            ).update(process_instance_info)
            logger.info(f'变量更新完成')
        else:
            # todo handle is cache
            obj = VariableInstance(**variable_info)
            self.session.add(obj)
            logger.info('变量插入完成')
        self.session.commit()

    def get_variable(self, process_instance_id: str, variable_key: str) -> Any:
        """
        获取变量值
        @param process_instance_id:流程实例id
        @param variable_key: 变量名称
        @return: variable value
        """
        obj = self.session.query(VariableInstance).filter(
            VariableInstance.process_instance_id == process_instance_id,
            VariableInstance.variable_key == variable_key).first()
        if not obj:
            raise VariableException(
                f'variable is not find by variable key {variable_key},'
                f'process instance id {process_instance_id}'
            )
        return VariableInfoSchema().dump(obj)

    @abstractmethod
    def handle_task_kwargs(self, task_kwargs: dict) -> dict:
        pass

    def handle_task_result(self, variable_configs: List[dict], task_result: dict, node_result_config: dict):
        """
        处理任务的返回值
        @param variable_configs:任务节点中配置的返回值
         {
            "variable_key": "add_result",
            "variable_value": "${add_result}",
            "variable_type": "int",
            "variable_desc": "add函数的返回值"
        }
        @param task_result:任务运行的实际返回值
        { "add_value": 12 }
        @param node_result_config:任务运行的实际返回值
        { "result_key":"add_value", "variable_key":"${add_result}" }
        @return:
        """
        if not node_result_config:
            return task_result
        node_variable_config_key = node_result_config.get('variable_key')
        node_variable_key = node_variable_config_key.replace('${', '').replace('}', '')
        result_key = node_result_config.get('result_key')

        for _variable_config in variable_configs:
            variable_config = copy.deepcopy(_variable_config)
            for _ in variable_config:
                variable_key = variable_config.get('variable_key')
                if variable_key == node_variable_key:
                    # 变量的类型
                    variable_type = variable_config.get('variable_type')
                    # 任务运行中真实的返回值
                    task_variable_value = task_result.get(result_key)
                    # 解析变量值
                    variable_operator = VariableOperator(node_variable_config_key, task_variable_value, variable_type)
                    real_variable_value = variable_operator.variable_operator()
                    # 替换变量值
                    variable_config['variable_value'] = real_variable_value
                    self.variable_insert(self.process_instance_id, variable_config)
                    break
        return task_result
