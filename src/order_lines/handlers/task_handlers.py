# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_handlers.py
# Time       ：2023/1/10 22:48
# Author     ：Y-aong
# version    ：python 3.7
# Description：
特定任务节点的处理
Processing of specific task nodes
"""
import traceback

from order_lines.handlers.base_handler import AbstractHandler
from order_lines.libraries.Group import Group, GroupParam
from order_lines.libraries.Parallel import Parallel, ParallelParam
from order_lines.libraries.ProcessControl import ProcessControl
from order_lines.utils.process_action_enum import StatusEnum
from public.logger import logger


class DefaultHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            func = getattr(module(), method_name)
            return func(task_kwargs)
        else:
            return super().handle(module, method_name, task_kwargs)


class CommonHandler(AbstractHandler):

    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            try:
                func = getattr(module(), method_name)
                result: dict = func(task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                return {'status': StatusEnum.red.value,
                        'error_info': f'error info:{e}\ntraceback:{traceback.format_exc()}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ProcessControlHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module(), method_name):
            try:
                task_id = ProcessControl().process_control(task_kwargs)
                return {'task_id': task_id, 'status': StatusEnum.green.value}
            except Exception as e:
                logger.error(f'The process control gateway is abnormal.error info:{e},'
                             f'\ntraceback:{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'traceback:{traceback.format_exc()}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class GroupHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: GroupParam) -> dict:

        if hasattr(module, method_name):
            process_info = task_kwargs.process_info
            process_node = task_kwargs.process_node
            try:
                result = Group(process_info, process_node).task_group(task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                logger.error(f'The task group fails to run.error info:{e},\n{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'traceback:{traceback.format_exc()}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ParallelHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: ParallelParam) -> dict:

        if hasattr(module, method_name):
            process_info = task_kwargs.process_info
            process_node = task_kwargs.process_node
            try:
                parallel = Parallel(process_info, process_node)
                result = parallel.parallel_task(task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                logger.error(f'The parallel gateway fails to run.error info:{e},\ntraceback:{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'traceback:{traceback.format_exc()}'}
        else:
            return super().handle(module, method_name, task_kwargs)
