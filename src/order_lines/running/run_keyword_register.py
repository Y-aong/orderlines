# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : run_keyword_register.py
# Time       ：2023/2/19 19:59
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import warnings

from order_lines.utils.utils import NormalizedDict


class _RunKeywordRegister:

    def __init__(self):
        self._libs = {}

    def register_run_keyword(self, libname, keyword, args_to_process,
                             deprecation_warning=True, dry_run=False):
        """
        这里还没有真正使用上
        """
        if libname not in self._libs:
            self._libs[libname] = NormalizedDict(ignore=['_'])
        self._libs[libname][keyword] = (int(args_to_process), dry_run)

    def get_args_to_process(self, libname, kwname):
        if libname in self._libs and kwname in self._libs[libname]:
            return self._libs[libname][kwname][0]
        return -1

    def get_dry_run(self, libname, kwname):
        if libname in self._libs and kwname in self._libs[libname]:
            return self._libs[libname][kwname][1]
        return False

    def is_run_keyword(self, libname, kwname):
        return self.get_args_to_process(libname, kwname) >= 0


RUN_KW_REGISTER = _RunKeywordRegister()
