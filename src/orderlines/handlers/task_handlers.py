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
import json
import traceback

from pydantic import BaseModel

from orderlines.handlers.base_handler import AbstractHandler
from orderlines.libraries.Group import Group, GroupParam
from orderlines.libraries.Parallel import Parallel, ParallelParam
from orderlines.libraries.ProcessControl import ProcessControl
from orderlines.utils.process_action_enum import TaskStatus
from orderlines.utils.utils import get_method_param_annotation
from public.logger import logger


class DefaultHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: BaseModel) -> dict:

        if hasattr(module, method_name):
            func = getattr(module(), method_name)
            return func(task_kwargs)
        else:
            return super().handle(module, method_name, task_kwargs)


class CommonHandler(AbstractHandler):

    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:

        if hasattr(module, method_name):
            try:
                flag, annotation = get_method_param_annotation(getattr(module, method_name))
                if not flag:
                    raise ValueError('plugin param is not pydantic type')
                task_kwargs = annotation(**task_kwargs)
                task_kwargs = self.handle_on_receive(task_kwargs, module, method_name)
                func = getattr(module(), method_name)
                result: dict = func(task_kwargs)
                result.setdefault('status', TaskStatus.green.value)
                return self.handle_on_success(result, module, method_name)
            except Exception as e:
                error = self.handle_on_failure(e, module, method_name)
                return {
                    'status': TaskStatus.red.value,
                    'error_info': json.dumps({'error info': str(error), 'traceback': traceback.format_exc()})
                }
        else:
            return super().handle(module, method_name, task_kwargs)


class ProcessControlHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: BaseModel) -> dict:

        if hasattr(module(), method_name):
            try:
                task_id = ProcessControl().process_control(task_kwargs)
                return {'task_id': task_id, 'status': TaskStatus.green.value}
            except Exception as e:
                logger.error(f'The process control gateway failure.error info:{e},'
                             f'\ntraceback:{traceback.format_exc()}')
                return {
                    'status': TaskStatus.red.value,
                    'error_info': json.dumps({'error info': e, 'traceback': traceback.format_exc()})
                }
        else:
            return super().handle(module, method_name, task_kwargs)


class GroupHandler(AbstractHandler):
    def handle(self, module, method_name: str, task_kwargs: GroupParam) -> dict:

        if hasattr(module, method_name):
            process_info = task_kwargs.process_info
            process_node = task_kwargs.process_node
            try:
                result = Group(process_info, process_node).task_group(task_kwargs)
                result.setdefault('status', TaskStatus.green.value)
                return result
            except Exception as e:
                logger.error(f'The task group failure.error info:{e},\n{traceback.format_exc()}')
                return {
                    'status': TaskStatus.red.value,
                    'error_info': json.dumps({'error info': e, 'traceback': traceback.format_exc()})
                }
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
                result.setdefault('status', TaskStatus.green.value)
                return result
            except Exception as e:
                logger.error(f'The parallel gateway failure.error info:{e},\ntraceback:{traceback.format_exc()}')
                return {'status': TaskStatus.red.value, 'error_info': f'traceback:{traceback.format_exc()}'}
        else:
            return super().handle(module, method_name, task_kwargs)


TASK_HANDLER = {
    'start': DefaultHandler(),
    'end': DefaultHandler(),
    'common': CommonHandler(),
    'process_control': ProcessControlHandler(),
    'parallel': ParallelHandler(),
    'group': GroupHandler(),
}
