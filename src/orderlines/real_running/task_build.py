# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : task_build.py
# Time       ：2023/8/1 10:27
# Author     ：YangYong
# version    ：python 3.10
# Description：
    创建任务
    build task
"""
from typing import List

from apis.orderlines.models import Variable
from apis.orderlines.schema.variable_schema import VariableInfoSchema
from orderlines.handlers.base_handler import AbstractHandler
from orderlines.handlers.task_handlers import TASK_HANDLER
from orderlines.real_running.running_check import CheckModule
from orderlines.utils.exceptions import OrderlinesHasNoTaskType
from orderlines.utils.orderlines_enum import TaskStatus
from orderlines.utils.utils import get_method_param_annotation
from orderlines.variable.variable_handler import VariableHandlerReal
from public.logger import logger


class TaskBuild:
    def __init__(self, process_instance_id: str, task_node: dict):
        self.process_instance_id = process_instance_id
        self.task_node = task_node
        self.module_check = CheckModule()

    def get_task_build_param(self):
        """
        获取创建任务所需要的函数, Gets the functions needed to create the task
        @return:
            task_kwargs: this is task kwargs
            task_build_param: build variable param
        """
        task_module = self.task_node.get('task_module')
        method_name = self.task_node.get('method_name')
        task_kwargs: dict = self.task_node.get('task_kwargs') or self.task_node.get('method_kwargs')
        task_config: dict = self.task_node.get('task_config')
        task_kwargs.setdefault('task_config', task_config)
        return task_kwargs, task_module, method_name

    def variable_config(self):
        from public.base_model import get_session
        session = get_session()
        variables = session.query(Variable).filter(
            Variable.process_id == self.task_node.get('process_id')
        ).distinct(Variable.variable_key).all()
        return VariableInfoSchema().dump(variables, many=True)

    async def build(self, task_id: str, process_info: dict, task_nodes: List[dict]) -> dict:
        """
        创建任务函数
        @param task_id:任务id
        @param process_info:流程信息
        @param task_nodes:任务节点
        @return:
        """
        return self.build_task(task_id, process_info, task_nodes)

    def build_task(
            self,
            task_id: str,
            process_info: dict,
            task_nodes: dict
    ) -> dict:
        """
        构建任务，并运行
        build task and run
        @param task_id: current task id
        @param process_info: process info
        @param task_nodes: process node info
        @return: task result
        """
        variable_handler = VariableHandlerReal(self.process_instance_id)
        task_type = self.task_node.get('task_type')
        task_handler: AbstractHandler = TASK_HANDLER.get(task_type)
        if not task_handler:
            raise OrderlinesHasNoTaskType(f'please check task type has no task type:{task_type}')
        task_kwargs, task_module, method_name = self.get_task_build_param()
        # 解析参数, parse task param
        logger.info(f'before param ::{task_kwargs}')
        task_kwargs = variable_handler.variable_handle_params(task_type, task_kwargs)
        logger.info(f'after param ::{task_kwargs}')
        if task_type in ['group', 'parallel', 'process_control']:
            task_kwargs['task_nodes'] = task_nodes
            task_kwargs['process_info'] = process_info
        self.module_check.check_module(task_module)
        module = self.module_check.modules.get(task_module)
        if task_module in ['Group', 'Parallel', 'ProcessControl']:
            flag, annotation = get_method_param_annotation(getattr(module, method_name))
            assert flag, 'task group and parallel params must be a pydantic param'
            task_kwargs.setdefault('task_id', task_id)
            task_result = task_handler.handle(module, method_name, annotation(**task_kwargs))
        else:
            task_result = task_handler.handle(module, method_name, task_kwargs)

        assert isinstance(task_result, dict), 'The task return value must be a dictionary'
        logger.info(f'parse return value {task_result}')
        # 解析返回值， parse return value
        task_result = variable_handler.variable_handle_result(
            task_type=task_type,
            variable_config=self.variable_config(),
            task_result=task_result,
            node_result_config=self.task_node.get('result_config')
        )
        task_result.setdefault('status', TaskStatus.green.value)
        return task_result
