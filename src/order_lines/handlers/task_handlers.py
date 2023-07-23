# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_handlers.py
# Time       ：2023/1/10 22:48
# Author     ：Y-aong
# version    ：python 3.7
# Description：具体任务节点的处理
"""
import traceback

from order_lines.handlers.base_handler import AbstractHandler
from order_lines.libraries.Group import Group, GroupType
from order_lines.libraries.Parallel import Parallel, ParallelType
from order_lines.libraries.ProcessControl import ProcessControl, ProcessControlType
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
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ProcessControlHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module(), method_name):
            try:
                print(f'process_control_param::{task_kwargs}')

                # process_control_param = ProcessControlType(**task_kwargs)
                task_id = ProcessControl().process_control(task_kwargs)
                return {'task_id': task_id, 'status': StatusEnum.green.value}
            except Exception as e:
                logger.error(f'流程控制运行异常::{e},\n{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class GroupHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: GroupType) -> dict:

        if hasattr(module, method_name):
            process_info = task_kwargs.process_info
            process_node = task_kwargs.process_node
            try:
                result = Group(process_info, process_node).task_group(task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                logger.error(f'任务组运行失败::{e}, \n{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)


class ParallelHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: ParallelType) -> dict:
        if hasattr(module, method_name):
            process_info = task_kwargs.process_info
            process_node = task_kwargs.process_node
            try:
                parallel = Parallel(process_info, process_node)
                result = parallel.parallel_task(task_kwargs)
                result.setdefault('status', StatusEnum.green.value)
                return result
            except Exception as e:
                logger.error(f'并行网关运行失败::{e}, \n堆栈信息::{traceback.format_exc()}')
                return {'status': StatusEnum.red.value, 'error_info': f'异常堆栈:{traceback.format_exc()}\n错误信息:{e}'}
        else:
            return super().handle(module, method_name, task_kwargs)
