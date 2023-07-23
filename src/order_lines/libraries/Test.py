# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Test.py
# Time       ：2023/1/10 21:09
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试的组件库
1、任务函数的参数必须增加**kw,因为流程运行中可能会有其他的参数
2、任务函数的返回值包含两个部分第一为运行状态，这里框架会自己处理，第二为自己的返回值，可以自定义
3、有返回值必须为dict字段方便扩展
"""
import time

from pydantic import Field

from conf.config import OrderLinesConfig
from order_lines.libraries.BaseTask import BaseTask
from order_lines.utils.base_orderlines_type import BasePluginResult, BasePluginParam


class TestType(BasePluginParam):
    a: int = Field(description='测试参数a')
    b: int = Field(description='测试参数b')


class Test(BaseTask):
    version = OrderLinesConfig.version

    def test_add(self, test_type: TestType, ) -> BasePluginResult:
        time.sleep(3)
        return {'add_value': test_type.a + test_type.b}

    def test_subtraction(self, test_type: TestType, ) -> BasePluginResult:
        return {'subtraction_value': test_type.a - test_type.b}

    def test_multi(self, test_type: TestType, ) -> BasePluginResult:
        return {'subtraction_value': test_type.a * test_type.b}
