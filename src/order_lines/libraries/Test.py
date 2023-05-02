# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Test.py
# Time       ：2023/1/10 21:09
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import time

from order_lines.libraries.BaseTask import BaseTask, run_keyword_variant


class Test(BaseTask):

    @run_keyword_variant('Test')
    def test_add(self, a: int, b: int, **kwargs) -> dict:
        time.sleep(10)
        return {'add_value': a + b}

    @run_keyword_variant('Test')
    def test_subtraction(self, a: int, b: int, **kwargs) -> dict:
        return {'subtraction_value': a - b}

    @run_keyword_variant('Test')
    def test_multi(self, a: int, b: int, **kwargs) -> dict:
        return {'subtraction_value': a * b}
