# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_handler.py
# Time       ：2023/1/10 20:31
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    使用责任链模式处理任务
    Use chain of responsibility mode handle task
"""
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    def handle(self, module: Any, method_name: str, task_kwargs: dict) -> dict:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    @staticmethod
    def handle_on_receive(param: Any, module, method_name: str):
        """
        处理函数参数
        @param param:
        @param module:
        @param method_name:
        @return:
        """
        if hasattr(module, 'on_receive'):
            receive_param = getattr(module(), 'on_receive')(param, method_name)
            return receive_param if receive_param else param

        return param

    @staticmethod
    def handle_on_success(result: Any, module: Any, method_name: str):
        if hasattr(module, 'on_success'):
            success_result = getattr(module(), 'on_success')(result, method_name)
            return success_result if success_result else result

        return result

    @staticmethod
    def handle_on_failure(error: str, module: Any, method_name: str):
        if hasattr(module, 'on_failure'):
            failure_error = getattr(module(), 'on_failure')(error, method_name)
            return failure_error if failure_error else error

        return error

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, module: Any, method_name: str, task_kwargs: BaseModel) -> dict:
        if self._next_handler:
            return self._next_handler.handle(module, method_name, task_kwargs)
        return {}
