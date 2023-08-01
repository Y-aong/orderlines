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
from orderlines.handlers.base_handler import AbstractHandler
from orderlines.handlers.task_handlers import TASK_HANDLER
from orderlines.real_running.app_context import AppContext
from orderlines.real_running.base_runner import BaseRunner
from orderlines.real_running.running_check import CheckModule
from orderlines.utils.exceptions import OrderlinesHasNoTaskType
from orderlines.utils.process_action_enum import StatusEnum
from orderlines.utils.utils import get_method_param_annotation


class TaskBuild(BaseRunner):
    def __init__(self, process_instance_id: str, context: AppContext):
        super(TaskBuild, self).__init__(process_instance_id, context)
        self.module_check = CheckModule()

    async def get_task_build_param(self, task_id):
        """获取创建任务所需要的函数, Gets the functions needed to create the task"""

        task_build_param = self.context.get_task_node_items(
            self.process_instance_id,
            task_id,
            'task_module',
            'method_name'
        )
        task_kwargs: dict = self.context.get_task_node_item(self.process_instance_id, task_id, 'method_kwargs')
        task_config: dict = self.task_config(task_id)
        task_kwargs.setdefault('task_config', task_config)
        return task_kwargs, task_build_param

    async def build(self, task_id: str) -> dict:
        """
        创建任务函数
        @param task_id:任务id
        @return:
        """
        task_type = self.context.get_task_node_item(self.process_instance_id, task_id, 'task_type')
        task_handler = TASK_HANDLER.get(task_type)
        if not task_handler:
            raise OrderlinesHasNoTaskType(f'please check task type has no task type:{task_type}')
        self.context.get_task_node_items(self.process_instance_id, task_id)
        task_kwargs, task_build_param = await self.get_task_build_param(task_id)

        if task_type in ['group', 'parallel', 'process_control']:
            task_kwargs['task_nodes'] = self.context.get_task_nodes(self.process_instance_id)
            task_kwargs['process_info'] = self.context.get_process_info(self.process_instance_id)

        return self._build_task(task_handler, task_kwargs=task_kwargs, **task_build_param)

    def _build_task(
            self,
            handler: AbstractHandler,
            task_module: str,
            method_name: str,
            task_kwargs: dict,
    ) -> dict:
        """
        构建任务，并运行
        build task and run
        @param handler: task handler
        @param task_module: task module
        @param method_name: method name
        @param task_kwargs: method run need params
        @return: task result
        """

        self.module_check.check_module(task_module)
        module = self.module_check.modules.get(task_module)
        if task_module in ['Group', 'Parallel', 'ProcessControl']:
            flag, annotation = get_method_param_annotation(getattr(module, method_name))
            assert flag, 'task group and parallel params must be a pydantic param'
            task_result = handler.handle(module, method_name, annotation(**task_kwargs))
        else:
            task_result = handler.handle(module, method_name, task_kwargs)

        assert isinstance(task_result, dict), 'The task return value must be a dictionary'
        task_result.setdefault('status', StatusEnum.green.value)
        return task_result
