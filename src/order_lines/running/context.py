# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : context.py
# Time       ：2023/2/19 20:15
# Author     ：blue_moon
# version    ：python 3.7
# Description：运行时的上下文，未真正实现，待开发
"""


class ExecutionContexts:

    def __init__(self):
        self._contexts = list()

    @property
    def current(self):
        return self._contexts[-1] if self._contexts else None

    @property
    def top(self):
        return self._contexts[0] if self._contexts else None

    def __iter__(self):
        return iter(self._contexts)

    @property
    def namespace(self):
        return (context.namespaec for context in self)


EXECUTION_CONTEXTS = ExecutionContexts()
