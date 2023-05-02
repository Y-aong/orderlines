# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_build.py
# Time       ：2023/2/26 22:02
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from typing import List

from order_lines.running.module_check import CheckModule
from order_lines.handlers.task_handlers import *

handler_context = {
    'start': DefaultHandler(),
    'end': DefaultHandler(),
    'common': CommonHandler(),
    'process_control': ProcessControlHandler(),
    'parallel': ParallelHandler(),
    'group': GroupHandler(),
}


async def build_task(process_node: List[dict], task_id: str, process_info):
    """
    从process_list中获取任务参数，组装为异步任务
    :param task_id:
    :param process_node:
    :param process_info:
    :return:
    """
    for node in process_node:
        task_type = node.get('task_type')
        if node.get('task_id') == task_id:
            _handler = handler_context.get(task_type)
            task_module = node.get('task_module')
            method_name = node.get('method_name')
            task_config = node.get('task_config') if node.get('task_config') else {}
            task_kwargs: dict = node.get('method_kwargs')
            task_kwargs = task_kwargs if task_kwargs else {}
            task_kwargs.setdefault('__task_config__', task_config)
            if task_type in ['group', 'parallel']:
                task_kwargs['process_node'] = process_node
                task_kwargs['process_info'] = process_info

            return await async_task(_handler, task_module, method_name, task_kwargs)


def sync_task(handler: AbstractHandler, task_module, method_name, task_kwargs):
    """
    将普通任务封装为同步任务
    :param handler:
    :param task_module:
    :param method_name:
    :param task_kwargs:
    :return:
    """
    module_check = CheckModule()
    module_check.check_module(task_module)
    module = module_check.modules.get(task_module)
    task_kwargs = task_kwargs if task_kwargs else {}
    if task_module == 'Group' or task_module == 'Parallel':
        task_result = handler.handle(module, method_name, task_kwargs)
    else:
        task_result = handler.handle(module, method_name, task_kwargs)
    assert isinstance(task_result, dict), '任务返回值必须为字典'
    task_result.setdefault('status', StatusEnum.green.value)
    return task_result


async def async_task(handler: AbstractHandler, task_module, method_name, task_kwargs):
    """将普通任务封装为异步任务"""
    return sync_task(handler, task_module, method_name, task_kwargs)
