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


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, module, method_name: str, task_kwargs: dict) -> dict:
        if self._next_handler:
            return self._next_handler.handle(module, method_name, task_kwargs)
        return {}
