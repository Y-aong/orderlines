# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : BuiltIn.py
# Time       ：2023/2/19 19:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""

from order_lines.libraries.BaseTask import run_keyword_variant, BaseTask


class BuiltIn(BaseTask):
    def __init__(self):
        super(BuiltIn, self).__init__()

    @run_keyword_variant('BuiltIn')
    def start(self, **kwargs):
        return {'status': self.success}

    @run_keyword_variant('BuiltIn')
    def end(self, **kwargs):
        return {'status': self.success}
