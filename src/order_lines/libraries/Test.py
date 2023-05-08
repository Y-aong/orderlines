# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Test.py
# Time       ：2023/1/10 21:09
# Author     ：blue_moon
# version    ：python 3.7
# Description：测试的组件库
1、任务函数的参数必须增加**kw,因为流程运行中可能会有其他的参数
2、任务函数的返回值包含两个部分第一为运行状态，这里框架会自己处理，第二为自己的返回值，可以自定义
3、有返回值必须为dict字段方便扩展
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
