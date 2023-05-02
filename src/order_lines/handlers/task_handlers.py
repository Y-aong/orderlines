# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_handlers.py
# Time       ：2023/1/10 22:48
# Author     ：blue_moon
# version    ：python 3.7
# Description：任务流程测试handler
"""
import traceback

from order_lines.handlers.base_handler import AbstractHandler
from order_lines.libraries.Group import Group
from order_lines.libraries.Parallel import Parallel
from order_lines.libraries.ProcessControl import ProcessControl
from order_lines.utils.process_action_enum import StatusEnum


class DefaultHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            func = getattr(module(), method_name)
            return func(**task_kwargs)
        else:
            return super().handle(module, method_name, task_kwargs)


class CommonHandler(AbstractHandler):

    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            try:
                func = getattr(module(), method_name)
                result: dict = func(**task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ProcessControlHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module(), method_name):
            try:
                task_id = ProcessControl().process_control(**task_kwargs)
                return {'task_id': task_id, 'status': StatusEnum.green.value}
            except Exception as e:
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class GroupHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            process_info = task_kwargs.get('process_info')
            process_node = task_kwargs.get('process_node')
            try:
                result = Group(process_info, process_node).task_group(**task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ParallelHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:
        if hasattr(module, method_name):
            process_info = task_kwargs.get('process_info')
            process_node = task_kwargs.get('process_node')
            try:
                parallel = Parallel(process_info, process_node)
                result = parallel.parallel_task(**task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)
