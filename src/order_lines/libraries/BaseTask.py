# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : BaseTask.py
# Time       ：2023/1/15 16:49
# Author     ：blue_moon
# version    ：python 3.7
# Description：base task 这里想做任务的动态注册
"""

from order_lines.utils.logger import logger
from order_lines.utils.process_action_enum import StatusEnum
from order_lines.running.context import EXECUTION_CONTEXTS
from order_lines.running.run_keyword_register import RUN_KW_REGISTER
from order_lines.utils.match import Matcher


class BaseTask:

    def __init__(self):
        self.success = StatusEnum.green.value
        self.error = StatusEnum.red.value

    @property
    def _context(self):
        return self._get_context()

    def _get_context(self, top=False):
        ctx = EXECUTION_CONTEXTS.current if not top else EXECUTION_CONTEXTS.top
        if ctx is None:
            raise AttributeError('Cannot access execution context')
        return ctx

    @property
    def _namespace(self):
        return self._get_context().namespace

    @property
    def _variables(self):
        return self._namespace.variables

    def _matches(self, string, pattern, caseless=False):
        # Must use this instead of fnmatch when string may contain newlines.
        matcher = Matcher(pattern, caseless=caseless, spaceless=False)
        return matcher.match(string)

    def _log_types(self, *args):
        self._log_types_at_level('DEBUG', *args)

    def _log_types_at_level(self, level, *args):
        msg = ["Argument types are:"] + [self._get_type(a) for a in args]
        logger.info(msg)

    def _get_type(self, arg):
        return str(type(arg))


def run_keyword_variant(class_name, resolve=1, dry_run=True):
    """运行组件库的变体实现,待实现"""
    def decorator(method):
        RUN_KW_REGISTER.register_run_keyword(class_name, method.__name__, resolve,
                                             deprecation_warning=False,
                                             dry_run=dry_run)
        return method

    return decorator
