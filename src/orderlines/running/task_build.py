# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_build.py
# Time       ：2023/2/26 22:02
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    创建任务
    build task
"""
from typing import List

from orderlines.running.module_check import CheckModule
from orderlines.handlers.task_handlers import DefaultHandler, \
    CommonHandler, ProcessControlHandler, ParallelHandler, GroupHandler, AbstractHandler
from orderlines.utils.process_action_enum import TaskStatus
from orderlines.utils.utils import get_method_param_annotation

handler_context = {
    'start': DefaultHandler(),
    'end': DefaultHandler(),
    'common': CommonHandler(),
    'process_control': ProcessControlHandler(),
    'parallel': ParallelHandler(),
    'group': GroupHandler(),
}


async def build_task(task_nodes: List[dict], task_id: str, process_info):
    """
    从process_list中获取任务参数，组装为异步任务
    :param task_id:
    :param task_nodes:
    :param process_info:
    :return:
    """
    for node in task_nodes:
        task_type = node.get('task_type')
        if node.get('task_id') == task_id:
            _handler = handler_context.get(task_type)
            task_module = node.get('task_module')
            method_name = node.get('method_name')
            task_config = node.get('task_config') if node.get('task_config') else {}
            task_kwargs: dict = node.get('method_kwargs')
            task_kwargs = task_kwargs if task_kwargs else {}
            task_kwargs.setdefault('task_config', task_config)
            if task_type in ['group', 'parallel', 'process_control']:
                task_kwargs['task_nodes'] = task_nodes
                task_kwargs['process_info'] = process_info

            return await async_task(_handler, task_module, method_name, task_kwargs)


def sync_task(handler: AbstractHandler, task_module, method_name, task_kwargs):
    """
    将普通任务封装为同步任务
    Encapsulate a common task as a synchronization task
    :param handler: handler
    :param task_module: task class module
    :param method_name: method name
    :param task_kwargs: task params
    :return:
    """
    module_check = CheckModule()
    module_check.check_module(task_module)
    module = module_check.modules.get(task_module)
    task_kwargs = task_kwargs if task_kwargs else {}
    if task_module == 'Group' or task_module == 'Parallel' or task_module == 'ProcessControl':
        flag, annotation = get_method_param_annotation(getattr(module, method_name))
        assert flag, 'task group and parallel params must be a pydantic param'
        task_result = handler.handle(module, method_name, annotation(**task_kwargs))
    else:
        task_result = handler.handle(module, method_name, task_kwargs)

    assert isinstance(task_result, dict), 'The task return value must be a dictionary'

    task_result.setdefault('status', TaskStatus.green.value)
    return task_result


async def async_task(handler: AbstractHandler, task_module, method_name, task_kwargs):
    return sync_task(handler, task_module, method_name, task_kwargs)
